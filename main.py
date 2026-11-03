import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageDraw, ImageTk

# ============================================================
# ELECTRONIC COMPONENT FINDER & MINI OSCILLOSCOPE
# Images are drawn by Python. No external image folder needed.
# ============================================================

DARK_THEME = {
    "bg": "#070B16", "header": "#111827", "panel": "#0F172A",
    "card": "#151E2F", "card2": "#1B2638", "text": "#F8FAFC",
    "muted": "#94A3B8", "border": "#26354D", "button": "#7C3AED",
    "button_text": "#FFFFFF", "graph": "#08111F", "grid": "#334155",
    "nav": "#111827", "accent": "#FF4D8D", "accent2": "#22D3EE"
}
LIGHT_THEME = {
    "bg": "#F4F7FB", "header": "#FFFFFF", "panel": "#FFFFFF",
    "card": "#FFFFFF", "card2": "#F8FAFC", "text": "#172033",
    "muted": "#64748B", "border": "#D7DFEA", "button": "#635BFF",
    "button_text": "#FFFFFF", "graph": "#FFFFFF", "grid": "#D9E1EA",
    "nav": "#FFFFFF", "accent": "#E83E8C", "accent2": "#0891B2"
}

components = {
    "Resistor": {
        "unit": "Ohm (Ω)",
        "description": "A resistor is an electronic component that limits or controls the flow of electric current.",
        "working": "When current passes through a resistor, it creates resistance and produces a voltage drop.",
        "applications": "Current limiting, voltage division, LED protection, biasing and signal control.",
        "role": "Controls current and voltage in an electronic circuit."
    },
    "Capacitor": {
        "unit": "Farad (F)",
        "description": "A capacitor is a component that stores electrical energy in an electric field.",
        "working": "It charges when voltage is applied and releases stored energy when required.",
        "applications": "Filtering, coupling, decoupling, timing circuits and energy storage.",
        "role": "Stores electrical energy and helps smooth or filter signals."
    },
    "Diode": {
        "unit": "Volt (V)",
        "description": "A diode is a semiconductor device that mainly allows current to flow in one direction.",
        "working": "It conducts current in forward bias and blocks current in reverse bias.",
        "applications": "Rectification, reverse-polarity protection, switching and signal detection.",
        "role": "Provides one-way current control in electronic circuits."
    },
    "LED": {
        "unit": "Volt (V)",
        "description": "An LED is a semiconductor device that emits visible or infrared light when current flows through it.",
        "working": "Electrical energy is converted into light energy when the LED is forward biased.",
        "applications": "Indicators, displays, lighting, status signals and decorative electronics.",
        "role": "Provides visual indication and converts electrical energy into light."
    },
    "Transistor": {
        "unit": "Volt (V)",
        "description": "A transistor is a semiconductor device commonly used for switching and amplification.",
        "working": "A small input signal can control a larger current through the transistor.",
        "applications": "Amplifiers, electronic switches, oscillators, digital circuits and signal processing.",
        "role": "Amplifies signals and works as an electronic switching device."
    }
}

def create_component_image(name):
    """Create a simple component illustration in memory; no image files are required."""
    img = Image.new("RGB", (500, 350), "#101827")
    d = ImageDraw.Draw(img)

    if name == "Resistor":
        d.line((35, 175, 155, 175), fill="#D1D5DB", width=9)
        d.line((345, 175, 465, 175), fill="#D1D5DB", width=9)
        d.rounded_rectangle((150, 125, 350, 225), radius=22,
                            fill="#D9A066", outline="white", width=4)
        for x, color in [(185, "#8B4513"), (225, "#E53935"),
                         (265, "#FDD835"), (305, "#6D4C41")]:
            d.rectangle((x, 125, x + 15, 225), fill=color)

    elif name == "Capacitor":
        d.line((220, 65, 220, 145), fill="#D1D5DB", width=9)
        d.line((280, 65, 280, 145), fill="#D1D5DB", width=9)
        d.line((115, 145, 385, 145), fill="#38BDF8", width=13)
        d.line((115, 205, 385, 205), fill="#38BDF8", width=13)
        d.line((220, 205, 220, 290), fill="#D1D5DB", width=9)
        d.line((280, 205, 280, 290), fill="#D1D5DB", width=9)

    elif name == "Diode":
        d.line((35, 175, 170, 175), fill="#D1D5DB", width=9)
        d.line((330, 175, 465, 175), fill="#D1D5DB", width=9)
        d.polygon([(170, 95), (170, 255), (330, 175)],
                  fill="#22D3EE", outline="white")
        d.line((330, 95, 330, 255), fill="white", width=12)

    elif name == "LED":
        d.line((220, 205, 220, 310), fill="#D1D5DB", width=9)
        d.line((280, 205, 280, 310), fill="#D1D5DB", width=9)
        d.polygon([(170, 210), (170, 100), (330, 155), (330, 210)],
                  fill="#EC4899", outline="white")
        d.line((330, 100, 330, 210), fill="white", width=10)
        d.line((285, 90, 345, 35), fill="#FDE047", width=7)
        d.polygon([(345, 35), (323, 42), (340, 58)], fill="#FDE047")
        d.line((345, 125, 405, 70), fill="#FDE047", width=7)
        d.polygon([(405, 70), (383, 77), (400, 93)], fill="#FDE047")

    elif name == "Transistor":
        d.ellipse((145, 65, 355, 285), fill="#7C3AED",
                  outline="white", width=5)
        d.line((250, 65, 250, 25), fill="#D1D5DB", width=9)
        d.line((250, 285, 250, 325), fill="#D1D5DB", width=9)
        d.line((145, 175, 75, 175), fill="#D1D5DB", width=9)
        d.line((250, 130, 300, 175), fill="white", width=8)
        d.line((300, 175, 250, 220), fill="white", width=8)
        d.line((250, 175, 185, 175), fill="white", width=8)

    return img

root = tk.Tk()
root.title("Electronic Component Finder & Mini Oscilloscope")
root.geometry("1280x900")
root.minsize(1100, 760)

dark_mode = True
theme = DARK_THEME
animation_running = False
animation_id = None
animation_phase = 0.0
current_page = 1

component_var = tk.StringVar(value="Resistor")
wave_type = tk.StringVar(value="Sine")
amplitude_value = tk.DoubleVar(value=5.0)
frequency_value = tk.DoubleVar(value=5.0)

def style_frame(widget, bg_key="card"):
    widget.configure(bg=theme[bg_key])

# Header
root.configure(bg=theme["bg"])
header = tk.Frame(root, bg=theme["header"], highlightbackground=theme["border"], highlightthickness=1)
header.pack(fill="x", padx=18, pady=(12, 5))
tk.Frame(header, bg=theme["accent"], height=5).pack(fill="x")
title = tk.Label(header, text="⚡ ELECTRONIC COMPONENT FINDER",
                 font=("Arial", 24, "bold"), bg=theme["header"], fg=theme["text"])
title.pack(pady=(10, 0))
subtitle = tk.Label(header, text="& MINI OSCILLOSCOPE", font=("Arial", 14, "bold"),
                    bg=theme["header"], fg=theme["accent"])
subtitle.pack()
tk.Frame(header, bg=theme["accent2"], height=2).pack(fill="x", padx=250, pady=4)
project_text = tk.Label(header,
    text="INTERACTIVE ECE PROJECT  •  COMPONENT INFORMATION  •  WAVEFORM ANALYSIS",
    font=("Arial", 9, "bold"), bg=theme["header"], fg=theme["muted"])
project_text.pack(pady=(0, 9))

page_container = tk.Frame(root, bg=theme["bg"])
page_container.pack(fill="both", expand=True, padx=18, pady=5)

# ---------------- COMPONENT PAGE ----------------
component_page = tk.Frame(page_container, bg=theme["bg"])
tk.Label(component_page, text="🔧  COMPONENT EXPLORER", font=("Arial", 20, "bold"),
         bg=theme["bg"], fg=theme["accent"]).pack(pady=(5, 5))
tk.Label(component_page,
         text="Select a component to explore its information, working and applications",
         font=("Arial", 10), bg=theme["bg"], fg=theme["muted"]).pack(pady=(0, 8))

selector_card = tk.Frame(component_page, bg=theme["card"],
                         highlightbackground=theme["border"], highlightthickness=1)
selector_card.pack(fill="x", padx=100, pady=5)
tk.Label(selector_card, text="SELECT COMPONENT", font=("Arial", 10, "bold"),
         bg=theme["card"], fg=theme["accent2"]).pack(side="left", padx=(18, 10), pady=10)

component_menu = tk.OptionMenu(selector_card, component_var, *components.keys())
component_menu.config(width=18, font=("Arial", 10, "bold"), bg=theme["button"],
                      fg="white", activebackground=theme["accent"],
                      activeforeground="white", highlightthickness=0)
component_menu["menu"].config(bg=theme["card"], fg=theme["text"],
                              activebackground=theme["accent"], activeforeground="white")
component_menu.pack(side="left", padx=10, pady=7)

component_main = tk.Frame(component_page, bg=theme["card"],
                          highlightbackground=theme["border"], highlightthickness=1)
component_main.pack(fill="both", expand=True, padx=55, pady=8)

image_section = tk.Frame(component_main, bg=theme["card2"], width=370,
                         highlightbackground=theme["border"], highlightthickness=1)
image_section.pack(side="left", fill="y", padx=10, pady=10)
image_section.pack_propagate(False)

component_name = tk.Label(image_section, text="RESISTOR", font=("Arial", 22, "bold"),
                          bg=theme["card2"], fg=theme["accent"])
component_name.pack(pady=(20, 4))
component_type_label = tk.Label(image_section, text="ELECTRONIC COMPONENT",
                                font=("Arial", 9, "bold"), bg=theme["card2"], fg=theme["muted"])
component_type_label.pack(pady=(0, 12))

image_box = tk.Frame(image_section, bg=theme["header"],
                     highlightbackground=theme["accent"], highlightthickness=2)
image_box.pack(padx=20, pady=8)
image_label = tk.Label(image_box, bg=theme["header"])
image_label.pack(padx=25, pady=25)

unit_display = tk.Label(image_section, text="Unit: Ohm (Ω)", font=("Arial", 12, "bold"),
                        bg=theme["card2"], fg=theme["accent"])
unit_display.pack(pady=10)
tk.Label(image_section, text="COMPONENT ROLE", font=("Arial", 9, "bold"),
         bg=theme["card2"], fg=theme["accent2"]).pack(pady=(12, 3))
role_small = tk.Label(image_section, text="", font=("Arial", 10), bg=theme["card2"],
                      fg=theme["muted"], wraplength=300, justify="center")
role_small.pack(padx=20, pady=4)

info_section = tk.Frame(component_main, bg=theme["card"])
info_section.pack(side="right", fill="both", expand=True, padx=20, pady=10)

def create_info_card(parent, heading, color):
    card = tk.Frame(parent, bg=theme["card2"], highlightbackground=color, highlightthickness=1)
    card.pack(fill="x", pady=7)
    heading_label = tk.Label(card, text=heading, font=("Arial", 11, "bold"),
                             bg=theme["card2"], fg=color)
    heading_label.pack(anchor="w", padx=14, pady=(9, 2))
    value_label = tk.Label(card, text="", font=("Arial", 10), bg=theme["card2"],
                           fg=theme["text"], wraplength=650, justify="left")
    value_label.pack(anchor="w", padx=14, pady=(3, 11))
    return card, heading_label, value_label

description_card, description_heading, description_value = create_info_card(info_section, "📘  DESCRIPTION", "#FF4D8D")
working_card, working_heading, working_value = create_info_card(info_section, "⚙  HOW IT WORKS", "#22D3EE")
application_card, application_heading, application_value = create_info_card(info_section, "📌  APPLICATIONS", "#D69E00")
role_card, role_heading, role_value = create_info_card(info_section, "💡  COMPONENT ROLE", "#A78BFA")

def show_component(*args):
    name = component_var.get()
    data = components[name]
    component_color = data.get("color_dark", theme["accent"]) if dark_mode else data.get("color_light", theme["accent"])

    component_name.config(text=name.upper(), fg=component_color)
    image_box.config(highlightbackground=component_color)
    unit_display.config(text="Unit: " + data["unit"], fg=component_color)
    description_value.config(text=data["description"])
    working_value.config(text=data["working"])
    application_value.config(text=data["applications"])
    role_value.config(text=data["role"])
    role_small.config(text=data["role"])

    for heading in [description_heading, working_heading, application_heading, role_heading]:
        heading.config(fg=component_color)

    # Draw the selected component image in memory; no image folder/files needed.
    img = create_component_image(name)
    img.thumbnail((250, 175))
    photo = ImageTk.PhotoImage(img)
    image_label.config(image=photo, text="")
    image_label.image = photo

component_var.trace_add("write", show_component)

# ---------------- OSCILLOSCOPE PAGE ----------------
scope_page = tk.Frame(page_container, bg=theme["bg"])
tk.Label(scope_page, text="📈  MINI OSCILLOSCOPE", font=("Arial", 20, "bold"),
         bg=theme["bg"], fg=theme["accent2"]).pack(pady=(5, 2))
tk.Label(scope_page, text="Change amplitude and frequency to observe real-time waveform variation",
         font=("Arial", 10), bg=theme["bg"], fg=theme["muted"]).pack(pady=(0, 7))

control_card = tk.Frame(scope_page, bg=theme["card"],
                        highlightbackground=theme["border"], highlightthickness=1)
control_card.pack(fill="x", padx=45, pady=5)

tk.Label(control_card, text="WAVEFORM", font=("Arial", 10, "bold"),
         bg=theme["card"], fg=theme["accent"]).grid(row=0, column=0, padx=12, pady=10)
wave_menu = tk.OptionMenu(control_card, wave_type, "Sine", "Cosine", "Square", "Triangle")
wave_menu.config(width=12, font=("Arial", 10, "bold"), bg=theme["button"],
                 fg="white", highlightthickness=0)
wave_menu["menu"].config(bg=theme["card"], fg=theme["text"])
wave_menu.grid(row=0, column=1, padx=5)

amplitude_text = tk.Label(control_card, text="AMPLITUDE", font=("Arial", 10, "bold"),
                           bg=theme["card"], fg="#D69E00")
amplitude_text.grid(row=0, column=2, padx=10)
amplitude_display = tk.Label(control_card, text="5.0 V", font=("Arial", 10, "bold"),
                             bg=theme["card"], fg="#D69E00", width=7)
amplitude_display.grid(row=0, column=4, padx=5)

frequency_text = tk.Label(control_card, text="FREQUENCY", font=("Arial", 10, "bold"),
                           bg=theme["card"], fg=theme["accent2"])
frequency_text.grid(row=1, column=2, padx=10)
frequency_display = tk.Label(control_card, text="5 Hz", font=("Arial", 10, "bold"),
                             bg=theme["card"], fg=theme["accent2"], width=7)
frequency_display.grid(row=1, column=4, padx=5)

graph_card = tk.Frame(scope_page, bg=theme["graph"],
                      highlightbackground=theme["accent2"], highlightthickness=1)
graph_card.pack(fill="both", expand=True, padx=45, pady=7)

fig, ax = plt.subplots(figsize=(9, 4), dpi=100)
fig.subplots_adjust(left=0.08, right=0.98, top=0.88, bottom=0.18)
canvas = FigureCanvasTkAgg(fig, master=graph_card)
canvas.get_tk_widget().pack(fill="both", expand=True)

measurement_frame = tk.Frame(scope_page, bg=theme["card"],
                             highlightbackground=theme["border"], highlightthickness=1)
measurement_frame.pack(fill="x", padx=45, pady=4)

measured_amplitude = tk.StringVar(value="Amplitude: -- V")
time_period_value = tk.StringVar(value="Time Period: -- s")
measured_frequency = tk.StringVar(value="Frequency: -- Hz")
rms_voltage = tk.StringVar(value="RMS: -- V")

measurement_labels = []
for col, (var, color) in enumerate([
    (measured_amplitude, "#FF4D8D"),
    (time_period_value, "#D69E00"),
    (measured_frequency, "#0891B2"),
    (rms_voltage, "#7C3AED")
]):
    label = tk.Label(measurement_frame, textvariable=var, font=("Arial", 10, "bold"),
                     bg=theme["card"], fg=color)
    label.grid(row=0, column=col, padx=28, pady=8)
    measurement_labels.append(label)

def generate_wave(t, amplitude, frequency, selected_wave, phase=0.0):
    angle = 2 * np.pi * frequency * t + phase
    if selected_wave == "Sine":
        return amplitude * np.sin(angle)
    if selected_wave == "Cosine":
        return amplitude * np.cos(angle)
    if selected_wave == "Square":
        return amplitude * np.where(np.sin(angle) >= 0, 1, -1)
    if selected_wave == "Triangle":
        # Smooth, symmetric triangle wave with peak values +amplitude and -amplitude.
        return amplitude * (2 / np.pi) * np.arcsin(np.sin(angle))
    return np.zeros_like(t)

wave_colors_dark = {"Sine": "#FF4D8D", "Cosine": "#A78BFA", "Square": "#22D3EE", "Triangle": "#FB923C"}
wave_colors_light = {"Sine": "#E83E8C", "Cosine": "#7C3AED", "Square": "#0891B2", "Triangle": "#EA580C"}

def show_waveform():
    amplitude = float(amplitude_value.get())
    frequency = float(frequency_value.get())
    selected_wave = wave_type.get()
    if amplitude <= 0 or frequency <= 0:
        return

    t = np.linspace(0, 1.0, 1800)
    y = generate_wave(t, amplitude, frequency, selected_wave, animation_phase)

    actual_amplitude = (np.max(y) - np.min(y)) / 2
    period = 1.0 / frequency
    if selected_wave in ("Sine", "Cosine"):
        rms = amplitude / np.sqrt(2)
    elif selected_wave == "Triangle":
        rms = amplitude / np.sqrt(3)
    else:
        rms = amplitude

    measured_amplitude.set(f"Amplitude: {actual_amplitude:.2f} V")
    time_period_value.set(f"Time Period: {period:.3f} s")
    measured_frequency.set(f"Frequency: {frequency:.0f} Hz")
    rms_voltage.set(f"RMS: {rms:.2f} V")

    if dark_mode:
        wave_color = wave_colors_dark[selected_wave]
        graph_background, graph_text, graph_muted, graph_grid = "#08111F", "#F8FAFC", "#94A3B8", "#334155"
    else:
        wave_color = wave_colors_light[selected_wave]
        graph_background, graph_text, graph_muted, graph_grid = "#FFFFFF", "#172033", "#64748B", "#D9E1EA"

    ax.clear()
    ax.plot(t, y, color=wave_color, linewidth=2.7)
    ax.plot(t, y, color=wave_color, linewidth=9, alpha=0.10)
    fig.patch.set_facecolor(graph_background)
    ax.set_facecolor(graph_background)
    ax.set_title(f"{selected_wave} Wave  •  Amplitude = {amplitude:.1f} V  •  Frequency = {frequency:.0f} Hz",
                 color=graph_text, fontsize=13, fontweight="bold")
    ax.set_xlabel("Time (seconds)", color=graph_muted)
    ax.set_ylabel("Voltage (V)", color=graph_muted)
    ax.tick_params(colors=graph_muted)
    ax.grid(True, color=graph_grid, alpha=0.55, linestyle="--", linewidth=0.7)
    ax.set_xlim(0, 1.0)
    ax.set_ylim(-amplitude * 1.25, amplitude * 1.25)
    ax.axhline(0, color=graph_grid, linewidth=0.8, alpha=0.8)
    for spine in ax.spines.values():
        spine.set_color(graph_grid)
    canvas.draw_idle()

def update_controls(value=None):
    amplitude_display.config(text=f"{amplitude_value.get():.1f} V")
    frequency_display.config(text=f"{frequency_value.get():.0f} Hz")
    if not animation_running:
        show_waveform()

# Refresh the graph immediately whenever the user selects Sine/Cosine/Square/Triangle.
wave_type.trace_add("write", lambda *_: show_waveform() if not animation_running else None)

amplitude_slider = tk.Scale(control_card, from_=0.5, to=20, resolution=0.5,
    orient="horizontal", variable=amplitude_value, command=update_controls,
    length=190, bg=theme["card"], fg=theme["text"], troughcolor="#CBD5E1",
    highlightthickness=0)
amplitude_slider.grid(row=0, column=3, padx=5)

frequency_slider = tk.Scale(control_card, from_=1, to=50, resolution=1,
    orient="horizontal", variable=frequency_value, command=update_controls,
    length=190, bg=theme["card"], fg=theme["text"], troughcolor="#CBD5E1",
    highlightthickness=0)
frequency_slider.grid(row=1, column=3, padx=5)

def animate_wave():
    global animation_phase, animation_id
    if not animation_running:
        animation_id = None
        return
    animation_phase += 0.18
    show_waveform()
    animation_id = root.after(40, animate_wave)

def start_animation():
    global animation_running
    if animation_running:
        return
    animation_running = True
    status_label.config(text="● LIVE", fg="#22C55E")
    animate_wave()

def stop_animation():
    global animation_running, animation_id
    animation_running = False
    if animation_id is not None:
        try:
            root.after_cancel(animation_id)
        except tk.TclError:
            pass
        animation_id = None
    status_label.config(text="● STOPPED", fg="#EF4444")

button_frame = tk.Frame(scope_page, bg=theme["bg"])
button_frame.pack(pady=4)

def make_action_button(parent, text, command, color, column):
    button = tk.Button(parent, text=text, command=command, font=("Arial", 10, "bold"),
        bg=color, fg="white", activebackground=color, relief="flat",
        width=12, padx=5, pady=5)
    button.grid(row=0, column=column, padx=5)
    return button

make_action_button(button_frame, "🔄 UPDATE", show_waveform, "#7C3AED", 0)
make_action_button(button_frame, "▶ START", start_animation, "#16A34A", 1)
make_action_button(button_frame, "⏹ STOP", stop_animation, "#DC2626", 2)

status_label = tk.Label(scope_page, text="● STOPPED", font=("Arial", 10, "bold"),
                        bg=theme["bg"], fg="#EF4444")
status_label.pack(pady=2)

# ---------------- NAVIGATION ----------------
navigation = tk.Frame(root, bg=theme["nav"])
navigation.pack(fill="x", padx=18, pady=(4, 10))

def show_page(page_number):
    global current_page
    current_page = page_number
    component_page.pack_forget()
    scope_page.pack_forget()
    if page_number == 1:
        component_page.pack(fill="both", expand=True)
        back_button.config(state="disabled")
        next_button.config(state="normal")
    else:
        scope_page.pack(fill="both", expand=True)
        back_button.config(state="normal")
        next_button.config(state="disabled")
        show_waveform()

def next_page():
    show_page(2)

def previous_page():
    show_page(1)

back_button = tk.Button(navigation, text="← COMPONENTS", command=previous_page,
    font=("Arial", 10, "bold"), bg="#E83E8C", fg="white",
    activebackground="#BE185D", relief="flat", width=15, pady=5)
back_button.pack(side="left", padx=10)

next_button = tk.Button(navigation, text="OSCILLOSCOPE →", command=next_page,
    font=("Arial", 10, "bold"), bg="#0891B2", fg="white",
    activebackground="#0E7490", relief="flat", width=15, pady=5)
next_button.pack(side="right", padx=10)

def apply_theme():
    t = theme
    root.config(bg=t["bg"])
    page_container.config(bg=t["bg"])
    navigation.config(bg=t["nav"])
    header.config(bg=t["header"], highlightbackground=t["border"])
    title.config(bg=t["header"], fg=t["text"])
    subtitle.config(bg=t["header"], fg=t["accent"])
    project_text.config(bg=t["header"], fg=t["muted"])

    component_page.config(bg=t["bg"])
    scope_page.config(bg=t["bg"])
    selector_card.config(bg=t["card"], highlightbackground=t["border"])
    selector_label.config(bg=t["card"], fg=t["accent2"])
    component_menu.config(bg=t["button"], fg="white")
    component_menu["menu"].config(bg=t["card"], fg=t["text"])
    component_main.config(bg=t["card"], highlightbackground=t["border"])
    image_section.config(bg=t["card2"], highlightbackground=t["border"])
    component_name.config(bg=t["card2"])
    component_type_label.config(bg=t["card2"], fg=t["muted"])
    image_box.config(bg=t["header"])
    image_label.config(bg=t["header"])
    unit_display.config(bg=t["card2"])
    role_small.config(bg=t["card2"], fg=t["muted"])
    info_section.config(bg=t["card"])
    for card in [description_card, working_card, application_card, role_card]:
        card.config(bg=t["card2"])
    for label in [description_heading, working_heading, application_heading, role_heading]:
        label.config(bg=t["card2"])
    for label in [description_value, working_value, application_value, role_value]:
        label.config(bg=t["card2"], fg=t["text"])

    control_card.config(bg=t["card"], highlightbackground=t["border"])
    wave_label.config(bg=t["card"])
    wave_menu.config(bg=t["button"])
    wave_menu["menu"].config(bg=t["card"], fg=t["text"])
    amplitude_text.config(bg=t["card"])
    amplitude_display.config(bg=t["card"])
    frequency_text.config(bg=t["card"])
    frequency_display.config(bg=t["card"])
    amplitude_slider.config(bg=t["card"], fg=t["text"])
    frequency_slider.config(bg=t["card"], fg=t["text"])
    graph_card.config(bg=t["graph"], highlightbackground=t["accent2"])
    measurement_frame.config(bg=t["card"], highlightbackground=t["border"])
    for label in measurement_labels:
        label.config(bg=t["card"])
    button_frame.config(bg=t["bg"])
    status_label.config(bg=t["bg"])
    theme_button.config(bg=t["button"])
    show_component()
    show_waveform()

def toggle_theme():
    global dark_mode, theme
    dark_mode = not dark_mode
    theme = DARK_THEME if dark_mode else LIGHT_THEME
    theme_button.config(text="☀  LIGHT MODE" if dark_mode else "🌙  DARK MODE")
    apply_theme()

theme_button = tk.Button(navigation, text="☀  LIGHT MODE", command=toggle_theme,
    font=("Arial", 10, "bold"), bg=theme["button"], fg="white",
    activebackground=theme["accent"], relief="flat", width=15, pady=5)
theme_button.pack(side="right", padx=10)

def reset_project():
    global animation_phase
    stop_animation()
    animation_phase = 0.0
    component_var.set("Resistor")
    wave_type.set("Sine")
    amplitude_value.set(5.0)
    frequency_value.set(5.0)
    amplitude_display.config(text="5.0 V")
    frequency_display.config(text="5 Hz")
    show_component()
    show_waveform()
    show_page(1)

reset_button = tk.Button(navigation, text="↻  RESET", command=reset_project,
    font=("Arial", 10, "bold"), bg="#EF4444", fg="white",
    activebackground="#B91C1C", relief="flat", width=15, pady=5)
reset_button.pack(side="right", padx=10)

# Initial display
show_component()
show_waveform()
show_page(1)

root.mainloop()
