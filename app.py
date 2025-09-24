from nicegui import ui, app
import sqlite3

# --- Database ---
def init_db():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_note_to_db(content: str):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()

def get_notes_from_db():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM notes ORDER BY id DESC")
    notes = cursor.fetchall()
    conn.close()
    return notes

def delete_note_from_db(note_id: int):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()

# --- UI ---
notes_container = None

def refresh_notes():
    notes_container.clear()
    for note_id, content in get_notes_from_db():
        with notes_container:
            with ui.card().classes("w-full mb-2"):
                ui.label(content)
                ui.button("🗑️ Delete", 
                          on_click=lambda _, i=note_id: (delete_note_from_db(i), 
                                                         refresh_notes()), 
                          color="red")

def add_note(content: str):
    if content.strip():
        add_note_to_db(content)
        note_input.value = ""
        refresh_notes()

init_db()

with ui.row().classes("w-full justify-center"):
    with ui.column().classes("w-1/2"):
        ui.label("📝 Simple Notes App").classes("text-2xl font-bold mb-4")
        note_input = ui.input("Write a new note...").props("clearable").\
            classes("w-full")
        ui.button("Add", on_click=lambda: add_note(note_input.value))
        notes_container = ui.column().classes("w-full mt-4")
        refresh_notes()

ui.run(title="Simple Notes App", reload=False)
