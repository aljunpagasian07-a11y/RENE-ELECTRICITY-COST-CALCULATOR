import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image


# Standard rate sa CDO
RATE_SA_CDO = 12.31

# ---------------- COLOR PALETTE ----------------
GREEN   = "#5d7b6f"   # primary background
DARKER  = "#4a6359"   # darker shade for the output card
CYAN    = "#D7F9FA"   # primary foreground (text, labels)
CYAN_HO = "#EAFDFE"   # hover tint



class Application:
    def __init__(self, root):
        self.root = root
        root.title("Rene Bituin - Electricity Cost Estimator")
        root.geometry("520x380")
        root.resizable(False, False)

        
        # ---------------- MAIN FRAME ----------------
        self.frame1 = ctk.CTkFrame(root, fg_color=GREEN, border_width=0,width=520, height=380, corner_radius=0)
        self.frame1.place(x=0, y=0)

        
        # ---------------- OUTPUT PANEL (rounded card) ----------------
        self.output_card = ctk.CTkFrame(
            self.frame1,
            fg_color=DARKER,
            width=210, height=350,                 # <-- rounded corners
            border_width=2,
            border_color=CYAN,
        )
        self.output_card.place(x=20, y=20)
        self.output_card.pack_propagate(False)


        self.result_text = tk.Text(
            self.output_card,
            bg=DARKER, fg=CYAN,
            relief="flat", borderwidth=0, highlightthickness=0,
            wrap="word", cursor="arrow",
            padx=10, pady=8,
            font=("Arial", 9),
            spacing1=1, spacing3=1,
            insertbackground=DARKER,
            selectbackground=GREEN, selectforeground=CYAN,
        )
        # Inset by a few pixels so the card's rounded corners show through
        self.result_text.place(x=6, y=6, relwidth=1.0, relheight=1.0,
                               width=-12, height=-12)
        self.result_text.configure(state="disabled")

        # ---------- TEXT TAGS ----------
        self.result_text.tag_config(
            "title", foreground=CYAN, justify="center",
            font=("Arial", 14, "bold"),
            spacing1=4, spacing3=2,
        )
        self.result_text.tag_config(
            "subtitle", foreground=CYAN, justify="center",
            font=("Arial", 8, "bold"),
            spacing3=6,
        )
        self.result_text.tag_config(
            "divider", foreground=CYAN, justify="center",
            font=("Arial", 8),
            spacing1=2, spacing3=6,
        )
        self.result_text.tag_config(
            "head", foreground=CYAN,
            font=("Arial", 9, "bold", "underline"),
            spacing1=4, spacing3=3,
        )
        self.result_text.tag_config(
            "body", foreground=CYAN,
            font=("Arial", 8),
        )
        self.result_text.tag_config(
            "cost", foreground=CYAN,
            font=("Arial", 9),
            spacing1=2,
        )
        self.result_text.tag_config(
            "big", foreground=CYAN, justify="center",
            font=("Arial", 12, "bold", "underline"),
            spacing1=4, spacing3=4,
        )
        self.result_text.tag_config(
            "foot", foreground=CYAN, justify="center",
            font=("Arial", 7, "italic"),
            spacing1=3,
        )

        self._show_placeholder()

        # ---------------- INPUTS ----------------
        self.label1 = ctk.CTkLabel(self.frame1, text="APPLIANCE NAME",
                                   text_color=CYAN,
                                   font=ctk.CTkFont(family="Helvetica", size=13, weight="bold"),
                                   width=130, height=20)
        self.label1.place(x=323, y=60)

        self.Appliance = ctk.CTkEntry(
            self.frame1, width=150, height=28,
            fg_color=CYAN, text_color=GREEN,
            border_color=CYAN, border_width=1,
            corner_radius=6,
        )
        self.Appliance.place(x=313, y=80)

        self.label2 = ctk.CTkLabel(self.frame1, text="WATTS",
                                   text_color=CYAN,
                                   font=ctk.CTkFont(family="Helvetica", size=13, weight="bold"),
                                   width=130, height=20)
        self.label2.place(x=323, y=130)

        self.Watts = ctk.CTkEntry(
            self.frame1, width=150, height=28,
            fg_color=CYAN, text_color=GREEN,
            border_color=CYAN, border_width=1,
            corner_radius=6,
        )
        self.Watts.place(x=313, y=150)

        self.label3 = ctk.CTkLabel(self.frame1, text="HOURS PER DAY USE",
                                   text_color=CYAN,
                                   font=ctk.CTkFont(family="Helvetica", size=13, weight="bold"),
                                   width=140, height=20)
        self.label3.place(x=320, y=200)

        self.Hours_per_day = ctk.CTkEntry(
            self.frame1, width=150, height=28,
            fg_color=CYAN, text_color=GREEN,
            border_color=CYAN, border_width=1,
            corner_radius=6,
        )
        self.Hours_per_day.place(x=313, y=220)

        self.Calculate = ctk.CTkButton(
            self.frame1, text="CALCULATE",
            command=self.on_Calculate,
            text_color=GREEN, fg_color=CYAN,
            hover_color=CYAN_HO,
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            corner_radius=6,
            width=96, height=32,
        )
        self.Calculate.place(x=340, y=260)

        for entry in (self.Appliance, self.Watts, self.Hours_per_day):
            entry.bind("<Return>", lambda event: self.on_Calculate())

        self.Appliance.focus_set()

    # ------------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------------
    def _render(self, lines):
        tb = self.result_text
        tb.configure(state="normal")
        tb.delete("1.0", "end")
        for text, tag in lines:
            tb.insert("end", text, tag)
        tb.configure(state="disabled")

    def _show_placeholder(self):
        self._render([
            ("\n\n",                          "body"),
            ("RENE BITUIN\n",                 "title"),
            ("ELECTRICITY COST ESTIMATOR\n",  "subtitle"),
            ("──────────────\n",              "divider"),
            ("\n",                            "body"),
            ("Enter the appliance details\n", "foot"),
            ("on the right, then press\n",    "foot"),
            ("CALCULATE.",                    "foot"),
        ])

    def _show_error(self, message):
        messagebox.showerror("Input Error", message)

    # ------------------------------------------------------------------
    # CALCULATE
    # ------------------------------------------------------------------
    def on_Calculate(self):
        appliance = self.Appliance.get().strip()
        watts_text = self.Watts.get().strip()
        hours_text = self.Hours_per_day.get().strip()

        # ---------- VALIDATION ----------
        if appliance == "":
            self._show_error("Please enter the appliance name.")
            self.Appliance.focus_set()
            return

        try:
            watts = float(watts_text)
        except ValueError:
            self._show_error("Power rating must be a number. (e.g. 60)")
            self.Watts.focus_set()
            return

        try:
            hours_per_day = float(hours_text)
        except ValueError:
            self._show_error("Hours per day must be a number. (e.g. 8)")
            self.Hours_per_day.focus_set()
            return

        if watts <= 0:
            self._show_error("Wala may watts na zero bay naunsa diay ka ulol")
            self.Watts.focus_set()
            return

        if hours_per_day < 0 or hours_per_day > 24:
            self._show_error("Bay, ang hours per day dapat 0 hangtod 24 ra.")
            self.Hours_per_day.focus_set()
            return

        # ---------- COMPUTATION ----------
        kw = watts / 1000
        daily_kw = kw * hours_per_day
        daily_cost = daily_kw * RATE_SA_CDO
        monthly_kwh = daily_kw * 30
        monthly_cost = daily_cost * 30

        # ---------- ROUND OFF ----------
        text_daily_kw = format(daily_kw, ".2f")
        text_daily_cost = format(daily_cost, ".2f")
        text_monthly_kwh = format(monthly_kwh, ".2f")
        text_monthly_cost = format(monthly_cost, ".2f")

        # ---------- BUILD REPORT ----------
        lines = [
            ("RENE BITUIN\n",                  "title"),
            ("ELECTRICITY COST ESTIMATOR\n",   "subtitle"),
            ("──────────────\n",               "divider"),

            ("APPLIANCE DETAILS\n",            "head"),
            ("Appliance : " + appliance + "\n",                    "body"),
            ("Power     : " + format(watts, ".2f") + " W\n",       "body"),
            ("Usage     : " + format(hours_per_day, ".2f") + " hrs/day\n", "body"),
            ("CDO Rate  : PHP " + format(RATE_SA_CDO, ".2f") + "/kWh\n",   "body"),

            ("\n",                             "body"),
            ("ESTIMATED ENERGY CONSUMPTION\n", "head"),
            ("Daily   : " + text_daily_kw + " kWh\n",    "body"),
            ("Monthly : " + text_monthly_kwh + " kWh\n", "body"),

            ("\n",                             "body"),
            ("ESTIMATED ELECTRICITY COST\n",   "head"),
            ("Daily   : PHP " + text_daily_cost + "\n",   "cost"),
            ("Monthly : PHP " + text_monthly_cost + "\n", "big"),

            ("\n",                             "body"),
            ("Estimate only | 30 days usage\n","foot"),
            ("Tagna-tagna lang ers, lab you bay!\n", "foot"),
        ]
        self._render(lines)


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    app = Application(root)
    root.mainloop()