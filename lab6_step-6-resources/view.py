import tkinter as tk
from tkinter import messagebox, font
from viewmodel import CalculatorViewModel
from PIL import Image, ImageTk
import pygame
import os
import sys


class CalculatorView:
    def __init__(self, root):
        self.root = root
        self.root.title("SimpleCalculatorMVVM")
        self.root.geometry("500x750")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.viewmodel = CalculatorViewModel()
        self.resources = {}

        # Initialisation des ressources
        self.setup_resources()
        self.setup_ui()

        # Gestion de la fermeture
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_resources(self):
        """Charge toutes les ressources (statiques et dynamiques)"""

        # === STATIC RESOURCES (chargement immédiat) ===
        try:
            # Chemin des ressources
            base_path = os.path.join(os.path.dirname(__file__), "resources")

            # 1. Icône de la fenêtre
            icon_path = os.path.join(base_path, "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
                print("Icône chargée avec succès")

            # 2. Logo
            logo_path = os.path.join(base_path, "logo.png")
            if os.path.exists(logo_path):
                self.resources['logo'] = ImageTk.PhotoImage(
                    Image.open(logo_path).resize((60, 60), Image.Resampling.LANCZOS)
                )
                print("Logo chargé avec succès")

            # 3. Police personnalisée
            self.resources['custom_font'] = font.Font(family="Helvetica", size=12, weight="bold")
            self.resources['display_font'] = font.Font(family="Helvetica", size=16)
            self.resources['history_font'] = font.Font(family="Helvetica", size=11)

            # 4. Curseurs
            self.resources['button_cursor'] = "hand2"
            self.resources['entry_cursor'] = "xterm"

            print("Ressources statiques chargées avec succès")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de chargement des ressources: {str(e)}")

        # === DYNAMIC RESOURCES (chargement à la demande) ===

        # 5. Son (chargement dynamique)
        try:
            pygame.mixer.init()
            sound_path = os.path.join(base_path, "click.wav")
            if os.path.exists(sound_path):
                self.resources['sound'] = pygame.mixer.Sound(sound_path)
                print("Son chargé avec succès")
            else:
                self.resources['sound'] = None
                print("Fichier son non trouvé")
        except Exception as e:
            print(f"Erreur d'initialisation du son: {str(e)}")
            self.resources['sound'] = None

        # 6. Animation GIF (chargement dynamique)
        self.resources['gif_frames'] = []
        self.resources['gif_index'] = 0
        try:
            gif_path = os.path.join(base_path, "animation.gif")
            if os.path.exists(gif_path):
                gif = Image.open(gif_path)
                self.resources['gif_delay'] = gif.info.get('duration', 100) / 1000

                frame = 0
                while True:
                    try:
                        gif.seek(frame)
                        self.resources['gif_frames'].append(
                            ImageTk.PhotoImage(gif.copy().resize((100, 50), Image.Resampling.LANCZOS))
                        )
                        frame += 1
                    except EOFError:
                        break
                print(f"Animation GIF chargée: {len(self.resources['gif_frames'])} frames")
        except Exception as e:
            print(f"Erreur de chargement du GIF: {str(e)}")

    def setup_ui(self):
        """Configure l'interface utilisateur"""

        # === MENU ===
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="О программе", command=self.show_about_dialog)
        file_menu.add_command(label="Очистить всё", command=self.clear)
        file_menu.add_command(label="Очистить историю", command=self.clear_history)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.on_closing)

        # Menu Ressources
        resources_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ресурсы", menu=resources_menu)
        resources_menu.add_command(label="Информация о ресурсах", command=self.show_resources_info)
        resources_menu.add_command(label="Воспроизвести звук", command=self.play_sound_test)

        # Main Frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # === LOGO ===
        if 'logo' in self.resources:
            logo_label = tk.Label(self.main_frame, image=self.resources['logo'], bg="#f0f0f0")
            logo_label.grid(row=0, column=0, columnspan=5, pady=5)

        # === CHAMP D'AFFICHAGE ===
        self.entry = tk.Entry(
            self.main_frame,
            width=28,
            font=self.resources.get('display_font', font.Font(family="Helvetica", size=16)),
            bd=0,
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
            relief="flat",
            cursor=self.resources['entry_cursor']
        )
        self.entry.grid(row=1, column=0, columnspan=5, pady=10, ipady=10, sticky="ew")
        self.entry.focus_set()

        # === HISTORIQUE ===
        self.history_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.history_frame.grid(row=2, column=0, columnspan=5, pady=10, sticky="ew")

        self.history = tk.Text(
            self.history_frame,
            height=6,
            width=28,
            font=self.resources.get('history_font', font.Font(family="Helvetica", size=11)),
            bg="#ffffff",
            fg="#000000",
            state='disabled',
            bd=0
        )
        self.history.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.history_frame, orient="vertical", command=self.history.yview)
        scrollbar.pack(side="right", fill="y")
        self.history['yscrollcommand'] = scrollbar.set

        # === ANIMATION GIF ===
        if self.resources['gif_frames']:
            self.animation_label = tk.Label(self.main_frame, bg="#f0f0f0")
            self.animation_label.grid(row=3, column=0, columnspan=5, pady=10)
            self.update_animation()

        # === CLAVIER ===
        button_list = [
            ('sin', 'cos', 'tan', 'ln', '%'),
            ('7', '8', '9', '/', '^'),
            ('4', '5', '6', '*', '√'),
            ('1', '2', '3', '-', '('),
            ('0', '.', '=', '+', ')')
        ]

        # Création des boutons
        row = 4
        for button_row in button_list:
            col = 0
            for button in button_row:
                if button in '0123456789.':
                    bg_color = "#d9d9d9"
                    active_bg = "#bfbfbf"
                elif button in '+-*/^':
                    bg_color = "#ff9500"
                    active_bg = "#cc7b00"
                elif button in 'sin cos tan ln √ %'.split():
                    bg_color = "#4a90d9"
                    active_bg = "#357abd"
                else:
                    bg_color = "#d9d9d9"
                    active_bg = "#bfbfbf"

                # Texte spécial pour certains boutons
                display_text = button
                if button == '√':
                    display_text = '√x'

                tk.Button(
                    self.main_frame,
                    text=display_text,
                    width=5,
                    height=2,
                    font=self.resources.get('custom_font', font.Font(family="Helvetica", size=12)),
                    bg=bg_color,
                    fg="#000000",
                    activebackground=active_bg,
                    bd=0,
                    relief="flat",
                    command=lambda x=button: self.click(x),
                    cursor=self.resources['button_cursor']
                ).grid(row=row, column=col, padx=5, pady=5)
                col += 1
            row += 1

        # === BOUTONS SPÉCIAUX ===
        special_row = row

        # Bouton C (Clear)
        tk.Button(
            self.main_frame,
            text="C",
            width=5,
            height=2,
            font=self.resources.get('custom_font', font.Font(family="Helvetica", size=12)),
            bg="#ff3b30",
            fg="#000000",
            activebackground="#cc2e26",
            bd=0,
            relief="flat",
            command=self.clear,
            cursor=self.resources['button_cursor']
        ).grid(row=special_row, column=0, padx=5, pady=10)

        # Bouton ⌫ (Backspace)
        tk.Button(
            self.main_frame,
            text="⌫",
            width=5,
            height=2,
            font=self.resources.get('custom_font', font.Font(family="Helvetica", size=12)),
            bg="#ff3b30",
            fg="#000000",
            activebackground="#cc2e26",
            bd=0,
            relief="flat",
            command=self.backspace,
            cursor=self.resources['button_cursor']
        ).grid(row=special_row, column=1, padx=5, pady=10)

        # Bouton CH (Clear History)
        tk.Button(
            self.main_frame,
            text="CH",
            width=5,
            height=2,
            font=self.resources.get('custom_font', font.Font(family="Helvetica", size=12)),
            bg="#ff3b30",
            fg="#000000",
            activebackground="#cc2e26",
            bd=0,
            relief="flat",
            command=self.clear_history,
            cursor=self.resources['button_cursor']
        ).grid(row=special_row, column=2, padx=5, pady=10)

        # === RACCOURCIS CLAVIER ===
        self.root.bind('<Key>', self.key_press)

    def update_animation(self):
        """Met à jour l'animation GIF"""
        if self.resources['gif_frames']:
            self.resources['gif_index'] = (self.resources['gif_index'] + 1) % len(self.resources['gif_frames'])
            self.animation_label.config(image=self.resources['gif_frames'][self.resources['gif_index']])
            self.root.after(int(self.resources.get('gif_delay', 0.1) * 1000), self.update_animation)

    def play_sound(self):
        """Joue un son (chargement dynamique)"""
        if self.resources.get('sound'):
            try:
                self.resources['sound'].play()
                print("Son joué")
            except Exception as e:
                print(f"Erreur de lecture du son: {str(e)}")

    def play_sound_test(self):
        """Test du son"""
        self.play_sound()
        messagebox.showinfo("Son", "Son de test joué!")

    def show_resources_info(self):
        """Affiche les informations sur les ressources"""
        info = "=== INFORMATIONS SUR LES RESSOURCES ===\n\n"
        info += "RESSOURCES STATIQUES (chargées au démarrage):\n"
        info += f"- Icône: {'✅' if os.path.exists('resources/icon.ico') else '❌'}\n"
        info += f"- Logo: {'✅' if 'logo' in self.resources else '❌'}\n"
        info += f"- Police: {'✅' if 'custom_font' in self.resources else '❌'}\n"
        info += f"- Curseurs: {'✅' if 'button_cursor' in self.resources else '❌'}\n\n"
        info += "RESSOURCES DYNAMIQUES (chargées à la demande):\n"
        info += f"- Son: {'✅' if self.resources.get('sound') else '❌'}\n"
        info += f"- Animation GIF: {'✅' if self.resources['gif_frames'] else '❌'} ({len(self.resources['gif_frames'])} frames)\n"

        messagebox.showinfo("Ressources", info)

    def show_about_dialog(self):
        """Affiche le dialogue À propos"""
        dialog = tk.Toplevel(self.root)
        dialog.title("О программе")
        dialog.geometry("350x250")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="#f0f0f0")

        # Logo dans le dialogue
        if 'logo' in self.resources:
            tk.Label(dialog, image=self.resources['logo'], bg="#f0f0f0").pack(pady=10)

        tk.Label(
            dialog,
            text="SimpleCalculatorMVVM",
            font=self.resources.get('custom_font', font.Font(family="Helvetica", size=14, weight="bold")),
            bg="#f0f0f0"
        ).pack(pady=5)

        tk.Label(
            dialog,
            text="Version: 1.0\nAuteur: Karim Atajanov\n\nRessources incluses:\n- Icône\n- Logo\n- Sons\n- Animation",
            font=self.resources.get('history_font', font.Font(family="Helvetica", size=11)),
            bg="#f0f0f0"
        ).pack(pady=10)

        tk.Button(
            dialog,
            text="Fermer",
            command=dialog.destroy,
            font=self.resources.get('custom_font', font.Font(family="Helvetica", size=12)),
            bg="#4a90d9",
            fg="white",
            activebackground="#357abd",
            bd=0,
            relief="flat",
            cursor=self.resources['button_cursor']
        ).pack(pady=10)

    def click(self, char):
        """Gère le clic sur un bouton"""
        # Jouer le son
        self.play_sound()

        # Remplacer les symboles spéciaux
        if char == '√':
            char = '√'
        elif char == '^':
            char = '^'
        elif char == '×':
            char = '*'
        elif char == '÷':
            char = '/'
        elif char == '−':
            char = '-'

        if char == '=':
            result = self.viewmodel.evaluate()
            self.update_entry()
            self.update_history()
            if self.viewmodel.get_error():
                messagebox.showerror("Erreur", f"Entrée invalide: {self.viewmodel.get_error()}")
        else:
            self.viewmodel.append_input(char)
            self.update_entry()

    def clear(self):
        """Efface tout"""
        self.viewmodel.clear()
        self.update_entry()
        self.play_sound()

    def backspace(self):
        """Supprime le dernier caractère"""
        self.viewmodel.backspace()
        self.update_entry()
        self.play_sound()

    def clear_history(self):
        """Efface l'historique"""
        self.viewmodel.clear_history()
        self.update_history()
        self.play_sound()

    def update_entry(self):
        """Met à jour le champ d'affichage"""
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.viewmodel.expression)

    def update_history(self):
        """Met à jour l'historique"""
        self.history.configure(state='normal')
        self.history.delete(1.0, tk.END)
        self.history.insert(tk.END, self.viewmodel.get_history())
        self.history.configure(state='disabled')
        self.history.see(tk.END)

    def key_press(self, event):
        """Gère les touches du clavier"""
        key = event.char

        if key in '0123456789.+−*/%^()':
            self.click(key)
        elif key == '\r':  # Enter
            self.click('=')
        elif key == '\x08':  # Backspace
            self.backspace()
        elif key.lower() == 'c':
            self.clear()
        elif key.lower() == 'h':
            self.clear_history()

    def on_closing(self):
        """Fermeture de l'application - déchargement des ressources"""
        try:
            # Décharger les ressources dynamiques
            if self.resources.get('sound'):
                self.resources['sound'] = None
                print("Son déchargé")

            pygame.mixer.quit()
            print("Mixer pygame fermé")

            # Vider les ressources
            self.resources.clear()
            print("Ressources déchargées")

        except Exception as e:
            print(f"Erreur lors du déchargement: {str(e)}")

        self.root.destroy()


# ========== MAIN ==========

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorView(root)
    root.mainloop()