import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

class FinanceTracker:
    def __init__(self, file_path="transactions.csv"):
        self.file_path = file_path
        self.transactions = []
        if not os.path.exists(file_path):
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Type", "Category", "Amount", "Description"])
        self.load_transactions()

    def load_transactions(self):
        self.transactions = []
        try:
            with open(self.file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Başlık satırı
                for row in reader:
                    if len(row) == 5:
                        self.transactions.append({
                            "date": row[0],
                            "type": row[1],
                            "category": row[2],
                            "amount": float(row[3]),
                            "description": row[4]
                        })
        except Exception as e:
            print(f"Yükleme hatası: {e}")

    def add_transaction(self, trans_type, category, amount, description):
        if trans_type not in ["Gelir", "Gider"]:
            raise ValueError("İşlem tipi 'Gelir' veya 'Gider' olmalı.")
        if amount <= 0:
            raise ValueError("Tutar pozitif olmalı.")
        
        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": trans_type,
            "category": category,
            "amount": amount,
            "description": description
        }
        self.transactions.append(transaction)
        with open(self.file_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                transaction["date"],
                transaction["type"],
                transaction["category"],
                transaction["amount"],
                transaction["description"]
            ])
        print("✅ İşlem eklendi.")

    def get_balance(self):
        balance = 0
        for t in self.transactions:
            if t["type"] == "Gelir":
                balance += t["amount"]
            else:
                balance -= t["amount"]
        return balance

    def get_summary_by_category(self):
        summary = {}
        for t in self.transactions:
            cat = t["category"]
            amt = t["amount"] if t["type"] == "Gelir" else -t["amount"]
            summary[cat] = summary.get(cat, 0) + amt
        return summary

    def plot_expenses(self):
        summary = self.get_summary_by_category()
        categories = []
        amounts = []

        for cat, amt in summary.items():
            if amt < 0:  # Sadece giderler
                categories.append(cat)
                amounts.append(-amt)

        if not categories:
            print("⚠️ Gider verisi bulunamadı. Lütfen önce gider ekleyin.")
            return

        plt.figure(figsize=(12, 6))
        plt.bar(categories, amounts, color='tomato', label='Gider')
        plt.title("Kategorilere Göre Gider Dağılımı", fontsize=14)
        plt.xlabel("Kategori", fontsize=12)
        plt.ylabel("Tutar (TL)", fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()

        desktop = r"C:\Users\suley\OneDrive\Masaüstü"
        filepath = os.path.join(desktop, "expenses_plot.png")
        try:
            plt.savefig(filepath, dpi=100, bbox_inches='tight')
            print(f"📊 Gider grafiği masaüstüne kaydedildi: {filepath}")
        except Exception as e:
            print(f"❌ Grafik kaydedilemedi: {e}")
        plt.show()

    def plot_incomes(self):
        summary = self.get_summary_by_category()
        categories = []
        amounts = []

        for cat, amt in summary.items():
            if amt > 0:  # Sadece gelirler
                categories.append(cat)
                amounts.append(amt)

        if not categories:
            print("⚠️ Gelir verisi bulunamadı. Lütfen önce gelir ekleyin.")
            return

        plt.figure(figsize=(12, 6))
        plt.bar(categories, amounts, color='limegreen', label='Gelir')
        plt.title("Kategorilere Göre Gelir Dağılımı", fontsize=14)
        plt.xlabel("Kategori", fontsize=12)
        plt.ylabel("Tutar (TL)", fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()

        desktop = r"C:\Users\suley\OneDrive\Masaüstü"
        filepath = os.path.join(desktop, "incomes_plot.png")
        try:
            plt.savefig(filepath, dpi=100, bbox_inches='tight')
            print(f"📊 Gelir grafiği masaüstüne kaydedildi: {filepath}")
        except Exception as e:
            print(f"❌ Grafik kaydedilemedi: {e}")
        plt.show()

    def export_to_csv(self, export_file="exported_transactions.csv"):
        desktop = r"C:\Users\suley\OneDrive\Masaüstü"
        if not os.path.exists(desktop):
            print(f"❌ Hata: Masaüstü dizini bulunamadı ({desktop}). Lütfen geçerli bir dizin belirtin.")
            return
        
        filepath = os.path.join(desktop, export_file)
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Type", "Category", "Amount", "Description"])
                for t in self.transactions:
                    writer.writerow([
                        t["date"],
                        t["type"],
                        t["category"],
                        t["amount"],
                        t["description"]
                    ])
            print(f"✅ Veriler başarıyla dışarı aktarıldı: {filepath}")
        except PermissionError:
            print(f"❌ Hata: '{filepath}' dosyasına yazma izni yok. Lütfen dizin izinlerini kontrol edin.")
        except Exception as e:
            print(f"❌ Dışarı aktarma hatası: {e}")

def main():
    tracker = FinanceTracker()

    while True:
        print("\n🔹 Kişisel Finans Takip")
        print("1. İşlem Ekle")
        print("2. Bakiyeyi Görüntüle")
        print("3. Kategori Özeti")
        print("4. Gider Grafiği Çiz")
        print("5. Gelir Grafiği Çiz")
        print("6. Verileri CSV'ye Aktar")
        print("7. Çıkış")

        try:
            secim = input("Seçiminiz (1-7): ").strip()
        except EOFError:
            print("Çıkılıyor...")
            break

        if secim == "1":
            try:
                tip = input("İşlem tipi (Gelir/Gider): ").strip()
                kategori = input("Kategori: ").strip()
                tutar = float(input("Tutar (örneğin 125.50): ").strip())
                aciklama = input("Açıklama: ").strip()
                tracker.add_transaction(tip, kategori, tutar, aciklama)
            except ValueError as e:
                print(f"Hata: {e}")
        elif secim == "2":
            bakiye = tracker.get_balance()
            print(f"💰 Bakiye: {bakiye:.2f} TL")
        elif secim == "3":
            print("📂 Kategori Özeti:")
            for kategori, tutar in tracker.get_summary_by_category().items():
                print(f"{kategori}: {tutar:.2f} TL")
        elif secim == "4":
            tracker.plot_expenses()
        elif secim == "5":
            tracker.plot_incomes()
        elif secim == "6":
            export_file = input("Dışarı aktarılacak dosya adı (ör. deneme.csv): ").strip()
            if not export_file:
                export_file = "exported_transactions.csv"
            if not export_file.endswith(".csv"):
                export_file += ".csv"
            tracker.export_to_csv(export_file)
        elif secim == "7":
            print("👋 Programdan çıkılıyor...")
            break
        else:
            print("❌ Geçersiz seçim.")

if __name__ == "__main__":
    main()