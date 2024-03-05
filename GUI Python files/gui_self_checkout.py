import tkinter as tk
import customtkinter
import customtkinter as ctk
from timer_service import TimerService
from statechart import Statechart
from PIL import Image, ImageTk
import pygame


class SelfCheckoutApp:
    def __init__(self, master, statechart):
        self.sc = statechart
        self.closed = False
        self.light_blinking_status = False
        self.master = root
        self.master.title("Self Checkout")
        self.master.geometry("800x800")

        pygame.mixer.init()

        self.label = tk.Label(self.master, font=("Helvetica", 18))
        self.label.pack_forget()

        # indicator light
        self.canvas = tk.Canvas(master, width=40, height=40)
        self.canvas.pack(pady=5)
        self.black_light = self.canvas.create_oval(5, 5, 40, 40, fill="black")
        self.red_light = self.canvas.create_oval(5, 5, 40, 40, fill="red", state="hidden")
        self.green_light = self.canvas.create_oval(5, 5, 40, 40, fill="green", state="hidden")

        # images
        self.power_off_image = Image.open('powerOff.jpg').resize((600, 600))
        self.welcome_image = Image.open('welcome.jpg').resize((600, 600))
        self.main_image = Image.open('main.jpg').resize((600, 600))
        self.help_image = Image.open('help.jpg').resize((600, 600))
        self.payment_image = Image.open('payment.jpg').resize((600, 600))
        self.posOn_image = Image.open('posOn.jpg').resize((600, 600))
        self.printer_image = Image.open('printer.jpg').resize((400, 700))

        # set current image
        self.current_image = ImageTk.PhotoImage(self.power_off_image)
        self.image_label = tk.Label(master, image=self.current_image)
        self.image_label.pack()

        # button declarations
        self.power_button = ctk.CTkButton(root, text="Power", command=self.power_pressed, corner_radius=20, width=10)
        self.power_button.pack(pady=10)

        self.guest_button = ctk.CTkButton(root, text="Guest", command=self.guest_pressed, corner_radius=20, width=10)
        self.guest_button.pack_forget()

        self.member_button = ctk.CTkButton(root, text="Member", command=self.member_pressed, corner_radius=20, width=10)
        self.member_button.pack_forget()

        self.barcode_button = ctk.CTkButton(root, text="Barcode detected", command=self.barcode_detected_pressed,
                                            corner_radius=20, width=10)
        self.barcode_button.pack_forget()

        self.help_button = ctk.CTkButton(root, text="Help", command=self.help_pressed, corner_radius=20, width=10)
        self.help_button.pack_forget()

        self.pay_button = ctk.CTkButton(root, text="Pay", command=self.pay_pressed, corner_radius=20, width=10)
        self.pay_button.pack_forget()

        self.enter_button = ctk.CTkButton(root, text="Enter", command=self.enter_pressed, corner_radius=20, width=10)
        self.enter_button.pack_forget()

        self.id_label = tk.Label(self.master, text="Enter ID number:", font=("", 16))
        self.id_label.pack_forget()

        self.id_entry = tk.Entry(self.master, font=("", 16), bd=2, width=10)
        self.id_entry.pack_forget()

        self.help_received_button = ctk.CTkButton(root, text="Help received", command=self.help_received_pressed,
                                                  corner_radius=20, width=10)
        self.help_received_button.pack_forget()

        self.confirm_button = ctk.CTkButton(root, text="Confirm", command=self.confirm_pressed,
                                            corner_radius=20, width=10)
        self.confirm_button.pack_forget()

        self.back_button = ctk.CTkButton(root, text="Back", command=self.back_pressed, corner_radius=20, width=10)
        self.back_button.pack_forget()

        self.insert_card_button = ctk.CTkButton(root, text="Insert Card", command=self.insert_card_pressed,
                                                corner_radius=20, width=10)
        self.insert_card_button.pack_forget()

        self.pin_label = tk.Label(self.master, text="Enter card PIN:", font=("", 16))
        self.pin_label.pack_forget()

        self.pin_entry = tk.Entry(self.master, font=("", 16), bd=2, width=10)
        self.pin_entry.pack_forget()

        self.tap_card_button = ctk.CTkButton(root, text="Tap Card", command=self.tap_card_pressed,
                                             corner_radius=20, width=10)
        self.tap_card_button.pack_forget()

        self.enter_pin_button = ctk.CTkButton(root, text="Enter", command=self.enter_pin_pressed,
                                              corner_radius=20, width=10)
        self.enter_pin_button.pack_forget()

    def set_to_red(self):
        # set the indicator light to red
        self.canvas.itemconfig(self.black_light, state="hidden")
        self.canvas.itemconfig(self.red_light, state="normal")
        self.canvas.itemconfig(self.green_light, state="hidden")

    def set_to_green(self):
        # set the indicator light to green
        self.canvas.itemconfig(self.black_light, state="hidden")
        self.canvas.itemconfig(self.red_light, state="hidden")
        self.canvas.itemconfig(self.green_light, state="normal")

    def power_pressed(self):
        # command for when the power button is pressed
        self.sc.raise_power_pressed()
        self.label.pack()
        self.guest_button.pack(pady=10)
        self.member_button.pack(pady=10)
        self.power_button.pack_forget()

    def guest_pressed(self):
        # command for when the guest button is pressed
        self.sc.raise_guest_pressed()
        self.remove_guest_member_buttons()
        self.display_guest_input()

    def member_pressed(self):
        # command for when the member button is pressed
        self.sc.raise_member_pressed()
        self.remove_guest_member_buttons()
        self.display_member_input()

    def remove_guest_member_buttons(self):
        # remove the guest button and member button from the interface
        self.guest_button.pack_forget()
        self.member_button.pack_forget()

    def display_guest_input(self):
        # show the barcode, help and pay buttons on the interface
        self.barcode_button.pack(pady=10)
        self.help_button.pack(pady=10)
        self.pay_button.pack(pady=10)

    def display_member_input(self):
        # show the id label, id entry and enter button on the interface
        self.id_label.pack(pady=10)
        self.id_entry.pack(pady=10)
        self.enter_button.pack(pady=10)

    def remove_member_input(self):
        # remove the id label and entry label from the display
        self.id_label.pack_forget()
        self.id_entry.pack_forget()

    def enter_pressed(self):
        # command for when the enter button is pressed
        self.sc.raise_id_entered()
        self.remove_member_input()
        self.display_guest_input()
        self.enter_button.pack_forget()
        self.label.pack_forget()

    def barcode_detected_pressed(self):
        # command for when the barcode detected button is pressed
        self.sc.raise_barcode_detected()
        pygame.mixer.music.load('scanner-beep.mp3')
        pygame.mixer.music.play()

    def blinking_lights(self):
        # Function to toggle the visibility of the lights to create a blinking effect
        if self.light_blinking_status is True:
            self.canvas.itemconfig(self.red_light, fill='red')
            self.master.after(500, self.reverse_lights)

    def reverse_lights(self):
        # Function to reverse the visibility of the lights
        if self.light_blinking_status is True:
            self.canvas.itemconfig(self.red_light, fill='white')
            self.master.after(500, self.blinking_lights)

    def help_pressed(self):
        # command for when the help button is pressed
        self.sc.raise_help_pressed()
        self.barcode_button.pack_forget()
        self.pay_button.pack_forget()
        self.help_button.pack_forget()
        self.help_received_button.pack(pady=10)
        self.light_blinking_status = True
        self.blinking_lights()

    def help_received_pressed(self):
        # command for when the help received button is pressed
        self.sc.raise_magnetic_card_swiped()
        self.barcode_button.pack(pady=10)
        self.help_button.pack(pady=10)
        self.pay_button.pack(pady=10)
        self.help_received_button.pack_forget()
        self.light_blinking_status = False
        self.canvas.itemconfig(self.red_light, fill='red')

    def pay_pressed(self):
        # command for when the pay button is pressed
        self.sc.raise_pay_pressed()
        self.barcode_button.pack_forget()
        self.pay_button.pack_forget()
        self.help_button.pack_forget()
        self.confirm_button.pack(pady=10)
        self.back_button.pack(pady=10)

    def confirm_pressed(self):
        # command for when the confirm button is pressed
        self.sc.raise_confirm_pressed()
        self.sc.raise_select_pay_type()
        self.pay_button.pack_forget()
        self.back_button.pack_forget()
        self.confirm_button.pack_forget()
        self.insert_card_button.pack(pady=10)
        self.tap_card_button.pack(pady=10)

    def back_pressed(self):
        # command for when the back button is pressed
        self.sc.raise_back_pressed()
        self.display_guest_input()
        self.confirm_button.pack_forget()
        self.back_button.pack_forget()

    def insert_card_pressed(self):
        # command for when the insert card button is pressed
        self.insert_card_button.pack_forget()
        self.tap_card_button.pack_forget()
        self.pin_label.pack(pady=10)
        self.pin_entry.pack(pady=10)
        self.enter_pin_button.pack(pady=10)

    def enter_pin_pressed(self):
        # command for when the enter pin button is pressed
        self.sc.raise_papproved()
        self.pin_label.pack_forget()
        self.pin_entry.pack_forget()
        self.enter_pin_button.pack_forget()
        pygame.mixer.music.load('printer-sound.mp3')
        pygame.mixer.music.play()

    def tap_card_pressed(self):
        # command for when the tap card button is pressed
        self.sc.raise_papproved()
        self.insert_card_button.pack_forget()
        self.tap_card_button.pack_forget()
        pygame.mixer.music.load('printer-sound.mp3')
        pygame.mixer.music.play()

    def set_text_label(self, text_label):
        # Function to change the text label of the interface
        self.label.pack_forget()
        self.label.config(text=text_label)
        self.label.pack(pady=10)

    def back_to_welcome_screen(self):
        # Function to show the welcome screen view in the interface
        self.image_label.pack(pady=10)
        self.guest_button.pack(pady=10)
        self.member_button.pack(pady=10)


if __name__ == "__main__":
    # Initialize statechart and timer service
    sc = Statechart()
    sc.timer_service = TimerService()

    # Set appearance mode and color theme for GUI
    customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

    # Create root window and GUI
    root = customtkinter.CTk()
    gui = SelfCheckoutApp(root, sc)
    sc.enter()

    # Main loop
    while not gui.closed:
        sc.run_cycle()

        # Update GUI based on current state
        if sc.is_state_active(Statechart.State.main_region_on_indicator_light_on_light_color_green):
            gui.set_to_green()

        if sc.is_state_active(Statechart.State.main_region_on_indicator_light_on_light_color_red):
            gui.set_to_red()

        if sc.is_state_active(Statechart.State.main_region_on_disaply_welcome_screen):
            gui.set_text_label("Please select mode to start purchase")
            gui.current_image = ImageTk.PhotoImage(gui.welcome_image)
            gui.image_label.configure(image=gui.current_image)
            gui.back_to_welcome_screen()

        if sc.is_state_active(Statechart.State.main_region_on_disaply_member_screen):
            gui.set_text_label("")

        if sc.is_state_active(Statechart.State.main_region_on_disaply_purchase_screen_psmain_screen):
            gui.set_text_label("Select a button to continue")
            gui.current_image = ImageTk.PhotoImage(gui.main_image)
            gui.image_label.configure(image=gui.current_image)

        if sc.is_state_active(Statechart.State.main_region_on_disaply_help_screen):
            gui.set_text_label("Assistance on its way!")
            gui.current_image = ImageTk.PhotoImage(gui.help_image)
            gui.image_label.configure(image=gui.current_image)

        if sc.is_state_active(Statechart.State.main_region_on_disaply_payment_screen):
            if sc.is_state_active(Statechart.State.main_region_on_user_mode_guest):
                gui.set_text_label("Total price is: $$$")
            else:
                gui.set_text_label("Total MEMBER price is: $$$\n\nYou earned 'XXX' points")
            gui.current_image = ImageTk.PhotoImage(gui.payment_image)
            gui.image_label.configure(image=gui.current_image)

        if sc.is_state_active(
                Statechart.State.main_region_on_disaply_payment_screen_pay_s_complete_payment_in_terminal_):
            gui.set_text_label("Please continue in the payment terminal")
            gui.current_image = ImageTk.PhotoImage(gui.posOn_image)
            gui.image_label.configure(image=gui.current_image)

        if sc.is_state_active(
                Statechart.State.main_region_on_disaply_payment_screen_pay_s_purchase_complete__thank_you_):
            gui.set_text_label("Printing Receipt...\n\nThank You for shopping with us!")
            gui.current_image = ImageTk.PhotoImage(gui.printer_image)
            gui.image_label.configure(image=gui.current_image)

        if sc.is_state_active(Statechart.State.main_region_on_disaply_purchase_screen_psitem_scanned):
            gui.set_text_label("Item Scanned :)")

        root.update()
