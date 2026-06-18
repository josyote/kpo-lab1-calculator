import tkinter as tk
from tkinter import messagebox, font
from viewmodel import CalculatorViewModel
from PIL import Image, ImageTk
import pygame
import os
import json
import logging


class CalculatorView:
    def __init__(self, root):
        self.root = root
        self.root.title("SimpleCalculatorMVVM")

        self.viewmodel = CalculatorViewModel()
        self.resources = {}

        # Charger la configuration
        self.config = self.load_config()

        # Appliquer la configuration
        self.apply_config()

        # Setup resources
        self.setup_resources()

        # Setup UI
        self.setup_ui()

        # Gestion de la fermeture
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_config(self):
        """Charge la configuration depuis config.json avec gestion d'erreurs"""
        default_config = {
            "window": {"width": 500, "height": 750},
            "background_color": "#f0f0f0",
            "font": {"name": "Helvetica", "size": 12},
            "sound_enabled": True,
            "animation": {"width": 100, "height": 50},
            "styles": {
                "default": {
                    "background_color": "#f0f0f0",
                    "button_color": "#d9d9d9",
                    "operator_color": "#ff9500",
                    "function_color": "#4a90d9",
                    "special_color": "#ff3b30",
                    "text_color": "#000000",
                    "font_size": 12,
                    "display_bg": "#ffffff",
                    "history_bg": "#ffffff"
                }
            },
            "active_style": "default"
        }

        try:
            config_path = os.path.join(os.path.dirname(__file__), "config.json")
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            # Vérifier la présence des clés obligatoires
            required_keys = ["window", "background_color", "font", "sound_enabled",
                             "animation", "styles", "active_style"]

            for key in required_keys:
                if key not in config:
                    logging.error(f"Clé manquante dans config.json: {key}")
                    return default_config

            return config

        except FileNotFoundError:
            logging.error("Fichier config.json non trouvé. Utilisation de la config par défaut.")
            messagebox.showwarning("Avertissement",
                                   "Fichier config.json non trouvé.\nUtilisation de la configuration par défaut.")
            return default_config

        except json.JSONDecodeError:
            logging.error("Format JSON invalide dans config.json.")
            messagebox.showerror("Erreur",
                                 "Format JSON invalide dans config.json.\nUtilisation de la configuration par défaut.")
            return default_config

        except Exception as e:
            logging.error(f"Erreur de chargement de config.json: {str(e)}")
            messagebox.showerror("Erreur",
                                 f"Erreur de chargement de config.json: {str(e)}")
            return default_config

    def apply_config(self):
        """Applique les paramètres de configuration"""
        try:
            # Taille de la fenêtre
            width = self.config["window"]["width"]
            height = self.config["window"]["height"]
            self.root.geometry(f"{width}x{height}")

            # Couleur de fond
            self.root.configure(bg=self.config["background_color"])

            # Style actif
            self.active_style = self.config.get("active_style", "default")

            # Vérifier si le style existe
            if self.active_style not in self.config["styles"]:
                logging.warning(f"Style '{self.active_style}' non trouvé. Utilisation de 'default'.")
                self.active_style = "default"

        except Exception as e:
            logging.error(f"Erreur d'application de la configuration: {str(e)}")

    def setup_resources(self):
        """Charge les ressources avec gestion d'erreurs"""
        style = self.config["styles"][self.active_style]
        base_path = os.path.join(os.path.dirname(__file__), "resources")

        try:
            # --- RESSOURCES STATIQUES ---

            # 1. Icône de la fenêtre
            icon_path = os.path.join(base_path, "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)

            # 2. Logo
            logo_path = os.path.join(base_path, "logo.png")
            if os.path.exists(logo_path):
                self.resources['logo'] = ImageTk.PhotoImage(
                    Image.open(logo_path).resize((60, 60), Image.Resampling.LANCZOS)
                )

            # 3. Police personnalisée (avec taille du style)
            self.resources['custom_font'] = font.Font(
                family=self.config["font"]["name"],
                size=style["font_size"],
                weight="bold"
            )

            self.resources['display_font'] = font.Font(
                family=self.config["font"]["name"],
                size=16
            )

            self.resources['history_font'] = font.Font(
                family=self.config["font"]["name"],
                size=11
            )

            # 4. Curseurs
            self.resources['button_cursor'] = "hand2"
            self.resources['entry_cursor'] = "xterm"

            print("Ressources statiques chargées avec succès")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de chargement des ressources: {str(e)}")

        # --- RESSOURCES DYNAMIQUES ---

        # 5. Son (selon configuration)
        if self.config["sound_enabled"]:
            try:
                pygame.mixer.init()
                sound_path = os.path.join(base_path, "click.wav")
                if os.path.exists(sound_path):
                    self.resources['sound'] = pygame.mixer.Sound(sound_path)
                    print("Son chargé avec succès")
                else:
                    self.resources['sound'] = None
            except Exception as e:
                print(f"Erreur d'initialisation du son: {str(e)}")
                self.resources['sound'] = None

        # 6. Animation GIF
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
                            ImageTk.PhotoImage(gif.copy().resize(
                                (self.config["animation"]["width"],
                                 self.config["animation"]["height"]),
                                Image.Resampling.LANCZOS
                            ))
                        )
                        frame += 1
                    except EOFError:
                        break
                print(f"Animation GIF chargée: {len(self.resources['gif_frames'])} frames")
        except Exception as e:
            print(f"Erreur de chargement du GIF: {str(e)}")

    def setup_ui(self):
        """Configure l'interface utilisateur"""
        style = self.config["styles"][self.active_style]

        # --- MENU ---
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

        # Menu Style
        style_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Стиль", menu=style_menu)

        # Ajouter les styles disponibles
        for style_name in self.config["styles"].keys():
            style_menu.add_command(
                label=style_name.replace("_", " ").title(),
                command=lambda s=style_name: self.change_style(s)
            )

        # Menu Ressources
        resources_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ресурсы", menu=resources_menu)
        resources_menu.add_command(label="Info ressources", command=self.show_resources_info)
        resources_menu.add_command(label="Tester le son", command=self.play_sound_test)

        # --- MAIN FRAME ---
        self.main_frame = tk.Frame(self.root, bg=style["background_color"])
        self.main_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # --- LOGO ---
        if 'logo' in self.resources:
            logo_label = tk.Label(
                self.main_frame,
                image=self.resources['logo'],
                bg=style["background_color"]
            )
            logo_label.grid(row=0, column=0, columnspan=5, pady=5)

        # --- CHAMP D'AFFICHAGE ---
        self.entry = tk.Entry(
            self.main_frame,
            width=28,
            font=self.resources.get('display_font', font.Font(family="Helvetica", size=16)),
            bd=0,
            bg=style["display_bg"],
            fg=style["text_color"],
            insertbackground=style["text_color"],
            relief="flat",
            cursor=self.resources['entry_cursor']
        )
        self.entry.grid(row=1, column=0, columnspan=5, pady=10, ipady=10, sticky="ew")
        self.entry.focus_set()

        # --- HISTORIQUE ---
        self.history_frame = tk.Frame(self.main_frame, bg=style["background_color"])
        self.history_frame.grid(row=2, column=0, columnspan=5, pady=10, sticky="ew")

        self.history = tk.Text(
            self.history_frame,
            height=6,
            width=28,
            font=self.resources.get('history_font', font.Font(family="Helvetica", size=11)),
            bg=style["history_bg"],
            fg=style["text_color"],
            state='disabled',
            bd=0
        )
        self.history.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.history_frame, orient="vertical", command=self.history.yview)
        scrollbar.pack(side="right", fill="y")
        self.history['yscrollcommand'] = scrollbar.set

        # --- ANIMATION GIF ---
        if self.resources['gif_frames']:
            self.animation_label = tk.Label(self.main_frame, bg=style["background_color"])
            self.animation_label.grid(row=3, column=0, columnspan=5, pady=10)
            self.update_animation()

        # --- CLAVIER ---
        button_list = [
            ('sin', 'cos', 'tan', 'ln', '%'),
            ('7', '8', '9', '/', '^'),
            ('4', '5', '6', '*', '√'),
            ('1', '2', '3', '-', '('),
            ('0', '.', '=', '+', ')')
        ]

        row = 4
        for button_row in button_list:
            col = 0
            for button in button_row:
                # Déterminer le style du bouton
                if button in '0123456789.':
                    bg_color = style["button_color"]
                    active_bg = self._darken_color(style["button_color"])
                elif button in '+-*/^%':
                    bg_color = style["operator_color"]
                    active_bg = self._darken_color(style["operator_color"])
                elif button in ['sin', 'cos', 'tan', 'ln', '√']:
                    bg_color = style["function_color"]
                    active_bg = self._darken_color(style["function_color"])
                else:
                    bg_color = style["button_color"]
                    active_bg = self._darken_color(style["button_color"])

                display_text = "√x" if button == '√' else button

                tk.Button(
                    self.main_frame,
                    text=display_text,
                    width=5,
                    height=2,
                    font=self.resources.get('custom_font', font.Font(family="Helvetica", size=12)),
                    bg=bg_color,
                    fg=style["text_color"],
                    activebackground=active_bg,
                    bd=0,
                    relief="flat",
                    command=lambda x=button: self.click(x),
                    cursor=self.resources['button_cursor']
                ).grid(row=row, column=col, padx=5, pady=5)
                col += 1
            row += 1

        # --- BOUTONS SPÉCIAUX ---
        special_row = row

        tk.Button(
            self.main_frame,
            text="C",
            width=5,
            height=2,
            font=self.resources.get('custom_font', font.Font(family="Helvetica", size=12)),
            bg=style["special_color"],
            fg=style["text_color"],
            activebackground=self._darken_color(style["special_color"]),
            bd=0,
            relief="flat",
            command=self.clear,
            cursor=self.resources['button_cursor']
        ).grid(row=special_row, column=0, padx=5, pady=10)

        tk.Button(
            self.main_frame,
            text="⌫",
            width=5,
            height=2,
            font=self.resources.get('custom_font', font.Font(family="Helvetica", size=12)),
            bg=style["special_color"],
            fg=style["text_color"],
            activebackground=self._darken_color(style["special_color"]),
            bd=0,
            relief="flat",
            command=self.backspace,
            cursor=self.resources['button_cursor']
        ).grid(row=special_row, column=1, padx=5, pady=10)

        tk.Button(
            self.main_frame,
            text="CH",
            width=5,
            height=2,
            font=self.resources.get('custom_font', font.Font(family="Helvetica", size=12)),
            bg=style["special_color"],
            fg=style["text_color"],
            activebackground=self._darken_color(style["special_color"]),
            bd=0,
            relief="flat",
            command=self.clear_history,
            cursor=self.resources['button_cursor']
        ).grid(row=special_row, column=2, padx=5, pady=10)

        # --- RACCOURCIS CLAVIER ---
        self.root.bind('<Key>', self.key_press)

    def _darken_color(self, color: str) -> str:
        """Assombrit une couleur hexadécimale"""
        try:
            # Enlever le #
            color = color.lstrip('#')
            # Convertir en RGB
            r, g, b = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
            # Assombrir
            r = max(0, r - 30)
            g = max(0, g - 30)
            b = max(0, b - 30)
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return "#888888"

    def change_style(self, style_name: str):
        """Change le style de l'application"""
        if style_name in self.config["styles"]:
            self.config["active_style"] = style_name
            self.apply_config()

            # Recréer l'interface
            self.main_frame.destroy()
            self.setup_ui()

            messagebox.showinfo("Style changé",
                                f"Style changé en: {style_name.replace('_', ' ').title()}")

            # Sauvegarder la configuration
            self.save_config()

    def save_config(self):
        """Sauvegarde la configuration actuelle"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), "config.json")
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            print("Configuration sauvegardée")
        except Exception as e:
            logging.error(f"Erreur de sauvegarde de la configuration: {str(e)}")

    def update_animation(self):
        """Met à jour l'animation GIF"""
        if self.resources['gif_frames']:
            self.resources['gif_index'] = (self.resources['gif_index'] + 1) % len(self.resources['gif_frames'])
            self.animation_label.config(image=self.resources['gif_frames'][self.resources['gif_index']])
            self.root.after(int(self.resources.get('gif_delay', 0.1) * 1000), self.update_animation)

    def play_sound(self):
        """Joue un son"""
        if self.config["sound_enabled"] and self.resources.get('sound'):
            try:
                self.resources['sound'].play()
            except Exception as e:
                print(f"Erreur de lecture du son: {str(e)}")

    def play_sound_test(self):
        """Test du son"""
        self.play_sound()
        messagebox.showinfo("Son", "Son de test joué!")

    def show_resources_info(self):
        """Affiche les informations sur les ressources"""
        style = self.config["styles"][self.active_style]
        info = "=== INFORMATIONS SUR LES RESSOURCES ===\n\n"
        info += f"Style actif: {self.active_style}\n"
        info += f"Couleur de fond: {style['background_color']}\n"
        info += f"Taille de police: {style['font_size']}\n\n"
        info += "RESSOURCES:\n"
        info += f"- Icône: {'✅' if os.path.exists('resources/icon.ico') else '❌'}\n"
        info += f"- Logo: {'✅' if 'logo' in self.resources else '❌'}\n"
        info += f"- Son: {'✅' if self.resources.get('sound') else '❌'}\n"
        info += f"- Animation: {'✅' if self.resources['gif_frames'] else '❌'} ({len(self.resources['gif_frames'])} frames)\n"

        messagebox.showinfo("Ressources", info)

    def show_about_dialog(self):
        """Affiche le dialogue À propos"""
        style = self.config["styles"][self.active_style]

        dialog = tk.Toplevel(self.root)
        dialog.title("О программе")
        dialog.geometry("350x280")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=style["background_color"])

        # Logo
        if 'logo' in self.resources:
            tk.Label(dialog, image=self.resources['logo'], bg=style["background_color"]).pack(pady=10)

        tk.Label(
            dialog,
            text="SimpleCalculatorMVVM",
            font=self.resources.get('custom_font', font.Font(family="Helvetica", size=14, weight="bold")),
            fg=style["text_color"],
            bg=style["background_color"]
        ).pack(pady=5)

        tk.Label(
            dialog,
            text=f"Version: 1.0\nAuteur: Karim Atajanov\n\nStyle actif: {self.active_style}\nPolice: {self.config['font']['name']} {style['font_size']}px",
            font=self.resources.get('history_font', font.Font(family="Helvetica", size=11)),
            fg=style["text_color"],
            bg=style["background_color"]
        ).pack(pady=10)

        tk.Button(
            dialog,
            text="Fermer",
            command=dialog.destroy,
            font=self.resources.get('custom_font', font.Font(family="Helvetica", size=12)),
            bg=style["button_color"],
            fg=style["text_color"],
            activebackground=self._darken_color(style["button_color"]),
            bd=0,
            relief="flat",
            cursor=self.resources['button_cursor']
        ).pack(pady=10)

    def click(self, char):
        """Gère le clic sur un bouton"""
        # Jouer le son
        self.play_sound()

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

    def backspace(self):
        """Supprime le dernier caractère"""
        self.viewmodel.backspace()
        self.update_entry()

    def clear_history(self):
        """Efface l'historique"""
        self.viewmodel.clear_history()
        self.update_history()

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
        """Fermeture de l'application"""
        try:
            # Sauvegarder la configuration
            self.save_config()

            # Décharger les ressources
            if self.resources.get('sound'):
                self.resources['sound'] = None

            pygame.mixer.quit()
            self.resources.clear()

        except Exception as e:
            print(f"Erreur lors de la fermeture: {str(e)}")

        self.root.destroy()


# ========== MAIN ==========

if __name__ == "__main__":
    # Configuration du logging
    log_path = os.path.join(os.path.dirname(__file__), "calculator.log")
    logging.basicConfig(
        filename=log_path,
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    root = tk.Tk()
    app = CalculatorView(root)
    root.mainloop()