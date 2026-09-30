import os
import tkinter as tk
from tkinter import messagebox


def get_filename():
    """Mengambil dan menormalisasi nama file dari entri input."""
    nama = entry_filename.get().strip()
    if not nama:
        return None
    return nama if nama.endswith(".txt") else f"{nama}.txt"


def handle_create():
    """1. Create: Membuat file teks baru dan menyimpan data awal."""
    filename = get_filename()
    if not filename:
        messagebox.showwarning("Peringatan", "Nama file tidak boleh kosong!")
        return

    content = txt_input.get("1.0", tk.END).strip()
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Sukses", f"File '{filename}' berhasil dibuat!")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal membuat file: {e}")


def handle_append():
    """2. Append: Menambahkan teks baru di baris akhir tanpa menimpa isi yang ada."""
    filename = get_filename()
    if not filename:
        messagebox.showwarning("Peringatan", "Tentukan nama file tujuan!")
        return

    content = txt_input.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Peringatan", "Teks yang akan ditambahkan tidak boleh kosong!")
        return

    try:
        
        prefix = "\n" if os.path.exists(filename) and os.path.getsize(filename) > 0 else ""
        with open(filename, "a", encoding="utf-8") as f:
            f.write(prefix + content)
        messagebox.showinfo("Sukses", f"Data berhasil ditambahkan ke '{filename}'.")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menambahkan data: {e}")


def handle_read():
    """4. Read: Mengambil dan menampilkan seluruh isi file ke area 'Tampil'."""
    filename = get_filename()
    if not filename or not os.path.exists(filename):
        messagebox.showerror("Error", f"File '{filename}' tidak ditemukan!")
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        txt_display.delete("1.0", tk.END)
        txt_display.insert(tk.END, content)
    except Exception as e:
        messagebox.showerror("Error", f"Gagal membaca file: {e}")


def handle_update():
    """3. Update: Mencari kata/teks lama dan menggantinya dengan informasi baru."""
    filename = get_filename()
    search_term = entry_search.get().strip()
    update_term = entry_update.get().strip()

    if not filename or not os.path.exists(filename):
        messagebox.showerror("Error", f"File '{filename}' tidak ditemukan!")
        return

    if not search_term:
        messagebox.showwarning("Peringatan", "Tentukan teks yang ingin diganti (Search text)!")
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        if search_term not in content:
            messagebox.showwarning("Peringatan", f"Teks '{search_term}' tidak ditemukan di '{filename}'.")
            return

        new_content = content.replace(search_term, update_term)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(new_content)

        messagebox.showinfo("Sukses", f"Teks '{search_term}' berhasil diubah menjadi '{update_term}'.")
        handle_read()  
    except Exception as e:
        messagebox.showerror("Error", f"Gagal memperbarui file: {e}")


def handle_delete():
    """5. Delete: Menghapus record/baris spesifik dalam file atau menghapus file itu sendiri."""
    target = entry_delete.get().strip()
    if not target:
        messagebox.showwarning("Peringatan", "Masukkan teks/data atau nama file yang ingin dihapus!")
        return

    
    target_file = target if target.endswith(".txt") else f"{target}.txt"
    if os.path.exists(target_file):
        os.remove(target_file)
        messagebox.showinfo("Sukses", f"Berkas '{target_file}' berhasil dihapus secara permanen.")
        return

    
    filename = get_filename()
    if not filename or not os.path.exists(filename):
        messagebox.showerror("Error", f"File '{filename}' tidak ditemukan.")
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        filtered_lines = [line for line in lines if target not in line]
        if len(filtered_lines) < len(lines):
            with open(filename, "w", encoding="utf-8") as f:
                f.writelines(filtered_lines)
            messagebox.showinfo("Sukses", f"Data berisi '{target}' berhasil dihapus dari '{filename}'.")
            handle_read()  
        else:
            messagebox.showwarning("Peringatan", f"Record '{target}' tidak ditemukan di '{filename}'.")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menghapus data: {e}")




root = tk.Tk()
root.title("FINAL PROJECT 1 GUI")
root.geometry("680x420")
root.resizable(False, False)


lbl_name = tk.Label(root, text="Nama file :", font=("Segoe UI", 9))
lbl_name.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4))

entry_filename = tk.Entry(root, width=20, font=("Segoe UI", 9))
entry_filename.insert(0, "")
entry_filename.grid(row=0, column=1, sticky="w", padx=5, pady=(12, 4))


lbl_teks = tk.Label(root, text="Teks :", font=("Segoe UI", 9))
lbl_teks.grid(row=1, column=0, sticky="w", padx=12, pady=(8, 2))

lbl_tampil = tk.Label(root, text="Tampil :", font=("Segoe UI", 9))
lbl_tampil.grid(row=1, column=3, sticky="w", padx=12, pady=(8, 2))


txt_input = tk.Text(root, width=28, height=8, font=("Segoe UI", 9))
txt_input.grid(row=2, column=0, columnspan=2, padx=(12, 5), pady=4, sticky="nsew")

frame_ca = tk.Frame(root)
frame_ca.grid(row=2, column=2, padx=8, pady=4)
btn_create = tk.Button(frame_ca, text="Create", width=9, font=("Segoe UI", 9), command=handle_create)
btn_create.pack(pady=4)
btn_append = tk.Button(frame_ca, text="Append", width=9, font=("Segoe UI", 9), command=handle_append)
btn_append.pack(pady=4)

txt_display = tk.Text(root, width=28, height=8, font=("Segoe UI", 9))
txt_display.grid(row=2, column=3, padx=(5, 8), pady=4, sticky="nsew")

btn_read = tk.Button(root, text="Read", width=8, font=("Segoe UI", 9), command=handle_read)
btn_read.grid(row=2, column=4, sticky="n", padx=(0, 12), pady=8)


lbl_search = tk.Label(root, text="Search text :", font=("Segoe UI", 9))
lbl_search.grid(row=3, column=0, sticky="w", padx=12, pady=(14, 2))

lbl_update = tk.Label(root, text="Update text :", font=("Segoe UI", 9))
lbl_update.grid(row=3, column=1, sticky="w", padx=12, pady=(14, 2))


entry_search = tk.Entry(root, width=18, font=("Segoe UI", 9))
entry_search.grid(row=4, column=0, sticky="w", padx=12, pady=2)

entry_update = tk.Entry(root, width=18, font=("Segoe UI", 9))
entry_update.grid(row=4, column=1, sticky="w", padx=12, pady=2)

btn_update = tk.Button(root, text="Update", width=9, font=("Segoe UI", 9), command=handle_update)
btn_update.grid(row=4, column=2, sticky="w", padx=8, pady=2)

lbl_del_file = tk.Label(root, text="File:", font=("Segoe UI", 9))
lbl_del_file.grid(row=5, column=0, sticky="w", padx=12, pady=(14, 2))

entry_delete = tk.Entry(root, width=18, font=("Segoe UI", 9))
entry_delete.grid(row=6, column=0, sticky="w", padx=12, pady=2)

btn_delete = tk.Button(root, text="Delete", width=9, font=("Segoe UI", 9), command=handle_delete)
btn_delete.grid(row=6, column=1, sticky="w", padx=12, pady=2)

root.mainloop()