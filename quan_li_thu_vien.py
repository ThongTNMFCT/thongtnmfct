import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import pandas as pd

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý thư viện")
        self.root.geometry("1000x700")
        
        # Cài đặt style cho các widget
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=6)
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TFrame", background="#F4F4F9")
        self.style.configure("Treeview", font=("Arial", 10), background="#ffffff", fieldbackground="#F4F4F9")
        self.style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#f0f0f0")
        
        self.books = []
        self.members = []
        self.borrow_records = []
        
        # Tạo Notebook để phân chia các Tab
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        # Tab Quản lý sách
        self.frame_books = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_books, text="Quản lý sách")

        # Tab Quản lý người mượn
        self.frame_members = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_members, text="Quản lý người mượn")

        # Tab Báo cáo
        self.frame_report = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_report, text="Báo cáo")

        self.create_widgets()

    def create_widgets(self):
        # Quản lý sách
        self.label_title = ttk.Label(self.frame_books, text="Tên sách:")
        self.label_title.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_title = ttk.Entry(self.frame_books, font=("Arial", 12))
        self.entry_title.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.label_author = ttk.Label(self.frame_books, text="Tác giả:")
        self.label_author.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_author = ttk.Entry(self.frame_books, font=("Arial", 12))
        self.entry_author.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.label_category = ttk.Label(self.frame_books, text="Thể loại:")
        self.label_category.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_category = ttk.Entry(self.frame_books, font=("Arial", 12))
        self.entry_category.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.label_available = ttk.Label(self.frame_books, text="Số lượng có sẵn:")
        self.label_available.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_available = ttk.Entry(self.frame_books, font=("Arial", 12))
        self.entry_available.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.btn_add_book = ttk.Button(self.frame_books, text="Thêm sách", command=self.add_book)
        self.btn_add_book.grid(row=4, column=0, padx=10, pady=10)

        self.btn_edit_book = ttk.Button(self.frame_books, text="Sửa sách", command=self.edit_book)
        self.btn_edit_book.grid(row=4, column=1, padx=10, pady=10)

        self.btn_delete_book = ttk.Button(self.frame_books, text="Xóa sách", command=self.delete_book)
        self.btn_delete_book.grid(row=4, column=2, padx=10, pady=10)

        # Treeview để hiển thị danh sách sách
        self.tree_books = ttk.Treeview(self.frame_books, columns=("Title", "Author", "Category", "Available"), show="headings")
        self.tree_books.heading("Title", text="Tên sách")
        self.tree_books.heading("Author", text="Tác giả")
        self.tree_books.heading("Category", text="Thể loại")
        self.tree_books.heading("Available", text="Còn lại")
        self.tree_books.grid(row=5, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Quản lý người mượn
        self.label_member_name = ttk.Label(self.frame_members, text="Tên người mượn:")
        self.label_member_name.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_member_name = ttk.Entry(self.frame_members, font=("Arial", 12))
        self.entry_member_name.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.btn_add_member = ttk.Button(self.frame_members, text="Thêm người mượn", command=self.add_member)
        self.btn_add_member.grid(row=1, column=0, padx=10, pady=10)

        self.btn_delete_member = ttk.Button(self.frame_members, text="Xóa người mượn", command=self.delete_member)
        self.btn_delete_member.grid(row=1, column=1, padx=10, pady=10)

        # Treeview để quản lý người mượn
        self.tree_members = ttk.Treeview(self.frame_members, columns=("Name"), show="headings")
        self.tree_members.heading("Name", text="Tên người mượn")
        self.tree_members.grid(row=2, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Mượn trả sách
        self.label_borrower = ttk.Label(self.frame_members, text="Người mượn:")
        self.label_borrower.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_borrower_name = ttk.Entry(self.frame_members, font=("Arial", 12))
        self.entry_borrower_name.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.label_borrow_date = ttk.Label(self.frame_members, text="Ngày mượn (DD/MM/YYYY):")
        self.label_borrow_date.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.entry_borrow_date = ttk.Entry(self.frame_members, font=("Arial", 12))
        self.entry_borrow_date.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.label_return_date = ttk.Label(self.frame_members, text="Ngày trả (DD/MM/YYYY):")
        self.label_return_date.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.entry_return_date = ttk.Entry(self.frame_members, font=("Arial", 12))
        self.entry_return_date.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.label_quantity = ttk.Label(self.frame_members, text="Số lượng sách:")
        self.label_quantity.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.entry_quantity = ttk.Entry(self.frame_members, font=("Arial", 12))
        self.entry_quantity.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        self.btn_borrow_book = ttk.Button(self.frame_members, text="Mượn sách", command=self.borrow_book)
        self.btn_borrow_book.grid(row=7, columnspan=2, pady=10)

        self.btn_return_book = ttk.Button(self.frame_members, text="Xác nhận đã trả sách", command=self.return_book)
        self.btn_return_book.grid(row=8, columnspan=2, pady=10)

        # Báo cáo
        self.btn_export_report = ttk.Button(self.frame_report, text="Xuất báo cáo", command=self.export_report)
        self.btn_export_report.pack(pady=20)

        # Căn chỉnh các widget
        self.frame_books.grid_rowconfigure(5, weight=1)
        self.frame_books.grid_columnconfigure(0, weight=1)
        self.frame_books.grid_columnconfigure(1, weight=1)
        self.frame_books.grid_columnconfigure(2, weight=1)
        self.frame_members.grid_rowconfigure(2, weight=1)
        self.frame_members.grid_columnconfigure(0, weight=1)
        self.frame_members.grid_columnconfigure(1, weight=1)

    def add_book(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        category = self.entry_category.get()
        available = self.entry_available.get()

        if title and author and category and available:
            available = int(available)
            self.books.append({"title": title, "author": author, "category": category, "available": available})
            self.update_books_treeview()
            self.clear_book_inputs()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin sách!")

    def edit_book(self):
        selected_item = self.tree_books.selection()
        if selected_item:
            selected_book = self.tree_books.item(selected_item[0])["values"]
            if selected_book:
                # Mở giao diện sửa sách
                self.entry_title.delete(0, "end")
                self.entry_title.insert(0, selected_book[0])
                self.entry_author.delete(0, "end")
                self.entry_author.insert(0, selected_book[1])
                self.entry_category.delete(0, "end")
                self.entry_category.insert(0, selected_book[2])
                self.entry_available.delete(0, "end")
                self.entry_available.insert(0, selected_book[3])

                # Xóa sách cũ và thay thế bằng sách mới
                self.delete_book(selected_item[0])

                # Đổi nút Thêm thành Sửa
                self.btn_add_book.config(text="Lưu sửa đổi", command=self.save_edited_book)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách để sửa!")

    def save_edited_book(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        category = self.entry_category.get()
        available = self.entry_available.get()

        if title and author and category and available:
            available = int(available)
            self.books.append({"title": title, "author": author, "category": category, "available": available})
            self.update_books_treeview()
            self.clear_book_inputs()
            self.btn_add_book.config(text="Thêm sách", command=self.add_book)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin sách!")

    def delete_book(self, item=None):
        if item:
            self.tree_books.delete(item)
        else:
            selected_item = self.tree_books.selection()
            if selected_item:
                book_title = self.tree_books.item(selected_item[0])["values"][0]
                self.books = [book for book in self.books if book["title"] != book_title]
                self.update_books_treeview()

    def update_books_treeview(self):
        for row in self.tree_books.get_children():
            self.tree_books.delete(row)

        for book in self.books:
            self.tree_books.insert("", "end", values=(book["title"], book["author"], book["category"], book["available"]))

    def add_member(self):
        name = self.entry_member_name.get()
        if name:
            self.members.append({"name": name})
            self.tree_members.insert("", "end", values=(name,))
            self.entry_member_name.delete(0, "end")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên người mượn!")

    def delete_member(self):
        selected_item = self.tree_members.selection()
        if selected_item:
            member_name = self.tree_members.item(selected_item[0])["values"][0]
            self.members = [member for member in self.members if member["name"] != member_name]
            self.tree_members.delete(selected_item[0])

    def borrow_book(self):
        borrower_name = self.entry_borrower_name.get()
        borrow_date = self.entry_borrow_date.get()
        return_date = self.entry_return_date.get()
        quantity = self.entry_quantity.get()

        try:
            borrow_date_obj = datetime.strptime(borrow_date, "%d/%m/%Y")
            return_date_obj = datetime.strptime(return_date, "%d/%m/%Y")
            quantity = int(quantity)

            # Giảm số lượng sách có sẵn
            available_books = [book for book in self.books if book["available"] > 0]
            if available_books and len(available_books) >= quantity:
                for i in range(quantity):
                    available_books[i]["available"] -= 1
                self.borrow_records.append({
                    "borrower": borrower_name,
                    "borrow_date": borrow_date_obj,
                    "return_date": return_date_obj,
                    "quantity": quantity
                })
                self.update_books_treeview()
                messagebox.showinfo("Thông báo", f"Sách đã được mượn bởi {borrower_name}!")
            else:
                messagebox.showwarning("Cảnh báo", "Không đủ sách để mượn!")
        except ValueError:
            messagebox.showerror("Lỗi", "Thông tin nhập không hợp lệ!")

    def return_book(self):
        selected_item = self.tree_members.selection()
        if selected_item:
            return_book_info = self.tree_members.item(selected_item[0])["values"]
            if return_book_info:
                # Xác nhận đã trả sách và tăng số lượng sách có sẵn
                for record in self.borrow_records:
                    if record["borrower"] == return_book_info[0]: 
                        for book in self.books:
                            book["available"] += record["quantity"]
                        self.update_books_treeview()
                        self.borrow_records.remove(record)
                        messagebox.showinfo("Thông báo", f"Sách đã được trả bởi {return_book_info[0]}!")
                        return
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn người mượn để trả sách!")

    def export_report(self):
        report = pd.DataFrame(self.books)
        report.to_excel("library_report.xlsx", index=False)
        messagebox.showinfo("Thông báo", "Báo cáo đã được xuất!")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
