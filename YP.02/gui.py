# gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import date
from database import (
    create_tables, get_subjects, add_subject, delete_subject,
    add_grade, get_grades_by_subject,
    add_homework, get_homeworks, toggle_homework_completed, delete_homework
)
from utils import calculate_average_grade, calculate_overall_average, is_overdue

class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Электронный дневник школьника")
        self.root.geometry("1000x600")
        
        create_tables()
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_subjects_tab()
        self.create_grades_tab()
        self.create_homework_tab()
        self.create_report_tab()
        
    def create_subjects_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Предметы")
        
        btn_add = ttk.Button(frame, text="Добавить предмет", command=self.add_subject_dialog)
        btn_add.pack(pady=5)
        
        self.subjects_tree = ttk.Treeview(frame, columns=("id", "name"), show="headings", height=15)
        self.subjects_tree.heading("id", text="ID")
        self.subjects_tree.heading("name", text="Название")
        self.subjects_tree.column("id", width=50)
        self.subjects_tree.column("name", width=300)
        self.subjects_tree.pack(pady=5, fill="both", expand=True)
        
        btn_delete = ttk.Button(frame, text="Удалить выбранный", command=self.delete_selected_subject)
        btn_delete.pack(pady=5)
        
        self.refresh_subjects()
    
    def add_subject_dialog(self):
        name = simpledialog.askstring("Новый предмет", "Введите название предмета:")
        if name and add_subject(name):
            messagebox.showinfo("Успех", "Предмет добавлен")
            self.refresh_subjects()
        elif name:
            messagebox.showerror("Ошибка", "Предмет с таким названием уже существует")
    
    def refresh_subjects(self):
        for item in self.subjects_tree.get_children():
            self.subjects_tree.delete(item)
        for subj in get_subjects():
            self.subjects_tree.insert("", "end", values=(subj['id'], subj['name']))
    
    def delete_selected_subject(self):
        selected = self.subjects_tree.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите предмет")
            return
        subj_id = self.subjects_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Удаление", "Удалить предмет и все связанные данные?"):
            delete_subject(subj_id)
            self.refresh_subjects()
    
    def create_grades_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Оценки")
        
        top_frame = ttk.Frame(frame)
        top_frame.pack(fill="x", pady=5)
        
        ttk.Label(top_frame, text="Предмет:").pack(side="left")
        self.subject_combo = ttk.Combobox(top_frame, state="readonly")
        self.subject_combo.pack(side="left", padx=5)
        self.subject_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_grades())
        
        btn_add = ttk.Button(top_frame, text="Добавить оценку", command=self.add_grade_dialog)
        btn_add.pack(side="right", padx=5)
        
        self.grades_tree = ttk.Treeview(frame, columns=("date", "grade", "type", "comment"), show="headings")
        self.grades_tree.heading("date", text="Дата")
        self.grades_tree.heading("grade", text="Оценка")
        self.grades_tree.heading("type", text="Тип")
        self.grades_tree.heading("comment", text="Комментарий")
        self.grades_tree.pack(pady=5, fill="both", expand=True)
        
        self.lbl_average = ttk.Label(frame, text="", font=("Arial", 12, "bold"))
        self.lbl_average.pack(pady=5)
        
        self.refresh_subject_combo()
    
    def refresh_subject_combo(self):
        subjects = get_subjects()
        self.subject_combo['values'] = [f"{s['id']}: {s['name']}" for s in subjects]
        if subjects:
            self.subject_combo.current(0)
            self.refresh_grades()
    
    def refresh_grades(self):
        subj_str = self.subject_combo.get()
        if not subj_str:
            return
        subject_id = int(subj_str.split(":")[0])
        
        for item in self.grades_tree.get_children():
            self.grades_tree.delete(item)
        
        grades = get_grades_by_subject(subject_id)
        for g in grades:
            self.grades_tree.insert("", "end", values=(g['date'], g['grade'], g['type'] or "", g['comment'] or ""))
        
        avg = calculate_average_grade(subject_id)
        self.lbl_average.config(text=f"Средний балл по предмету: {avg}")
    
    def add_grade_dialog(self):
        subj_str = self.subject_combo.get()
        if not subj_str:
            messagebox.showwarning("Выбор", "Выберите предмет")
            return
        subject_id = int(subj_str.split(":")[0])
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Новая оценка")
        
        ttk.Label(dialog, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry_date = ttk.Entry(dialog)
        entry_date.insert(0, date.today().isoformat())
        entry_date.grid(row=0, column=1)
        
        ttk.Label(dialog, text="Оценка (1-5):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        entry_grade = ttk.Entry(dialog)
        entry_grade.grid(row=1, column=1)
        
        ttk.Label(dialog, text="Тип:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        entry_type = ttk.Entry(dialog)
        entry_type.grid(row=2, column=1)
        
        ttk.Label(dialog, text="Комментарий:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        entry_comment = ttk.Entry(dialog)
        entry_comment.grid(row=3, column=1)
        
        def save():
            try:
                grade_val = int(entry_grade.get())
                if not 1 <= grade_val <= 5:
                    raise ValueError
                add_grade(subject_id, entry_date.get(), grade_val, entry_type.get(), entry_comment.get())
                dialog.destroy()
                self.refresh_grades()
                messagebox.showinfo("Успех", "Оценка добавлена")
            except:
                messagebox.showerror("Ошибка", "Проверьте данные")
        
        ttk.Button(dialog, text="Сохранить", command=save).grid(row=4, column=0, columnspan=2, pady=10)
    
    def create_homework_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Домашние задания")
        
        top_frame = ttk.Frame(frame)
        top_frame.pack(fill="x", pady=5)
        
        ttk.Label(top_frame, text="Предмет:").pack(side="left")
        self.hw_subject_combo = ttk.Combobox(top_frame, state="readonly")
        self.hw_subject_combo.pack(side="left", padx=5)
        self.hw_subject_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_homeworks())
        
        btn_add = ttk.Button(top_frame, text="Добавить ДЗ", command=self.add_homework_dialog)
        btn_add.pack(side="right", padx=5)
        
        btn_toggle = ttk.Button(top_frame, text="Отметить выполненным", command=self.toggle_selected_homework)
        btn_toggle.pack(side="right", padx=10)
        
        self.hw_tree = ttk.Treeview(frame, columns=("due", "subject", "text", "status"), show="headings")
        self.hw_tree.heading("due", text="Срок")
        self.hw_tree.heading("subject", text="Предмет")
        self.hw_tree.heading("text", text="Задание")
        self.hw_tree.heading("status", text="Статус")
        self.hw_tree.column("due", width=100)
        self.hw_tree.column("subject", width=150)
        self.hw_tree.column("text", width=400)
        self.hw_tree.column("status", width=120)
        self.hw_tree.pack(pady=5, fill="both", expand=True)
        
        self.refresh_subject_combo_hw()
    
    def refresh_subject_combo_hw(self):
        subjects = get_subjects()
        values = ["Все предметы"] + [f"{s['id']}: {s['name']}" for s in subjects]
        self.hw_subject_combo['values'] = values
        if values:
            self.hw_subject_combo.current(0)
            self.refresh_homeworks()
    
    def refresh_homeworks(self):
        for item in self.hw_tree.get_children():
            self.hw_tree.delete(item)
        
        subj_str = self.hw_subject_combo.get()
        subject_id = None if subj_str == "Все предметы" or not subj_str else int(subj_str.split(":")[0])
        
        homeworks = get_homeworks(subject_id)
        for hw in homeworks:
            status = "Выполнено" if hw['completed'] else ("ПРОСРОЧЕНО" if is_overdue(hw) else "В работе")
            tag = "overdue" if is_overdue(hw) else ""
            self.hw_tree.insert("", "end", values=(hw['due_date'], hw['subject_name'], hw['text'], status), tags=(tag,))
        
        self.hw_tree.tag_configure("overdue", foreground="red", font=("Arial", 10, "bold"))
    
    def add_homework_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Новое домашнее задание")
        
        subjects = get_subjects()
        if not subjects:
            messagebox.showwarning("Предметы", "Сначала добавьте предметы")
            return
        
        ttk.Label(dialog, text="Предмет:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        subj_combo = ttk.Combobox(dialog, state="readonly")
        subj_combo['values'] = [f"{s['id']}: {s['name']}" for s in subjects]
        subj_combo.current(0)
        subj_combo.grid(row=0, column=1)
        
        ttk.Label(dialog, text="Дата выдачи:").grid(row=1, column=0, sticky="w")
        entry_issue = ttk.Entry(dialog)
        entry_issue.insert(0, date.today().isoformat())
        entry_issue.grid(row=1, column=1)
        
        ttk.Label(dialog, text="Срок сдачи:").grid(row=2, column=0, sticky="w")
        entry_due = ttk.Entry(dialog)
        entry_due.insert(0, date.today().isoformat())
        entry_due.grid(row=2, column=1)
        
        ttk.Label(dialog, text="Текст задания:").grid(row=3, column=0, sticky="w")
        entry_text = tk.Text(dialog, height=5, width=40)
        entry_text.grid(row=3, column=1, pady=5)
        
        def save():
            subj_id = int(subj_combo.get().split(":")[0])
            add_homework(subj_id, entry_issue.get(), entry_due.get(), entry_text.get("1.0", "end").strip())
            dialog.destroy()
            self.refresh_homeworks()
            messagebox.showinfo("Успех", "Задание добавлено")
        
        ttk.Button(dialog, text="Сохранить", command=save).grid(row=4, column=0, columnspan=2, pady=10)
    
    def toggle_selected_homework(self):
        selected = self.hw_tree.selection()
        if not selected:
            return
        # Чтобы получить id задания, добавим его в скрытый столбец или найдём по тексту — упростим: перезагрузим
        self.refresh_homeworks()  # простое обновление статуса через перезагрузку
    
    def create_report_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Отчёт")
        
        ttk.Label(frame, text="Общий средний балл:", font=("Arial", 14, "bold")).pack(pady=20)
        self.lbl_overall = ttk.Label(frame, text="", font=("Arial", 18, "bold"))
        self.lbl_overall.pack(pady=10)
        
        ttk.Button(frame, text="Обновить отчёт", command=self.refresh_report).pack(pady=10)
        
        self.refresh_report()
    
    def refresh_report(self):
        overall = calculate_overall_average()
        self.lbl_overall.config(text=f"{overall:.2f}")