from modules.globalvar import GlobalVar

global_object = GlobalVar()

def checkbox_event(string_var: any, current_checkbox: str) -> None:
    current_value = string_var.get()

    if current_value != current_checkbox:
        string_var.set(current_checkbox)

def change_delay(event: any, label: any, entry: any, ctk: any) -> None:
    current_delay = entry.get()

    if current_delay is not None or current_delay != "":
        try:
            current_delay = int(current_delay)

            if current_delay > 0:
                global_animation_delay = current_delay
            else:
                print_logs_label(label, "Delay harus > 0", log_type = "err")
                entry.delete(0, ctk.END)
                entry.insert(0, global_animation_delay)
                return
        except Exception:
            entry.delete(0, ctk.END)
            entry.insert(0, global_animation_delay)
            return

def print_logs_label(label: any, message: str, text_color: str = global_object.fg_color, background: str = global_object.button_color, log_type: str = "log") -> None:
    if log_type == "err":
        message = f"[ Error ] - {message}"
    elif log_type == "log":
        message = f"{message}"
    else:
        return

    label.configure(text = message, text_color = text_color, bg_color = background)