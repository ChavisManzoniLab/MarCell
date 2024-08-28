import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import yaml
import time
import MarCell as mc

def initialise_project(path_to_tapas_scripts, specify_channel, scale_x, scale_y,zMin,zMax, path_to_folder, name_extraction, cellpose_name):
    mc.initialisation(path_to_folder, name_extraction)
    mc.change_channel(path_to_tapas_scripts, specify_channel)
    tapas_file = '01_tapas-preprocess-ROI.txt'
    pattern = 'process:scale'
    text_replacement = 'scalex:'+str(scale_x)+'\n'
    mc.change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

    tapas_file = '01_tapas-preprocess-ROI.txt'
    pattern = 'scalex:'+str(scale_x)
    text_replacement = 'scaley:'+str(scale_y)+'\n'
    mc.change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)
  
    tapas_file = '01_tapas-preprocess-ROI.txt'
    pattern = 'process:cropZ'
    text_replacement = 'zMin:'+str(zMin)+'\n'
    mc.change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

    tapas_file = '01_tapas-preprocess-ROI.txt'
    pattern = 'zMin:'
    text_replacement = 'zMax:'+str(zMax)+'\n'
    mc.change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)


    tapas_file = '02a_tapas-cellpose-reelin.txt'
    pattern = "process:calibration"
    text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\calibration\ \n"
    mc.change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

    tapas_file = '02a_tapas-cellpose-reelin.txt'
    pattern = "process:exe"
    text_replacement = 'dir:'+path_to_tapas_scripts + " \n"
    mc.change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

    pattern = "//name"
    text_replacement = 'file:'+cellpose_name + " \n"
    mc.change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

    tapas_file = 'all_measures_local.txt'
    pattern = "process:distanceLine"
    text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\distance\ \n"
    mc.change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

    tapas_file = 'all_measures_local.txt'
    pattern = "//coord"
    text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\coordinates\ \n"
    mc.change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

    tapas_file = 'all_measures_local.txt'
    pattern = "//volume"
    text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\volume\ \n"
    mc.change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

    tapas_file = 'all_measures_local.txt'
    pattern = "list:all"
    text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\intensity\ \n"
    mc.change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

    tapas_file = 'all_measures_local.txt'
    pattern = "process:calibrationSave"
    text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\calibration\ \n"
    mc.change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)
 
def open_project():
    folder_path = filedialog.askdirectory(title="Select a Project Folder")
    if folder_path:
        messagebox.showinfo("Project Opened", f"Opened project at: {folder_path}")

def save_convention(convention_name_entry, convention_entry, separator_entry):
    name = convention_name_entry.get()
    convention = convention_entry.get()
    separator = separator_entry.get()

    if not name:
        messagebox.showwarning("Input Error", "Convention name cannot be empty.")
        return

    if not convention:
        messagebox.showwarning("Input Error", "Convention entry cannot be empty.")
        return

    if not separator:
        messagebox.showwarning("Input Error", "Separator entry cannot be empty.")
        return

    try:
        convention_list = convention.split(',')
        with open('MarCell_data.yaml', 'r') as f:
            data = yaml.safe_load(f)
            if 'convention' not in data:
                data['convention'] = {}
            data['convention'][name] = {'convention': convention_list, 'separator': separator}

            # Save the updated data back to the YAML file
            with open('MarCell_data.yaml', 'w') as f:
                yaml.safe_dump(data, f)

            # Refresh the options in the OptionMenu
            refresh_options()

            messagebox.showinfo("Success", "Convention saved successfully!")
            convention_window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving: {e}")

def add_naming_convention():
    global convention_window
    convention_window = tk.Toplevel(root)
    convention_window.geometry('700x150')
    convention_window.title("Add a naming convention")
    convention_window.columnconfigure([0,1,2,3], weight=1, minsize=50)
    convention_window.rowconfigure([0,1,2,3], weight=1)

    tk.Label(convention_window, text="Convention name: ").grid(row=0, column=0, padx=10, pady=10, sticky='w')
    convention_name_entry = tk.Entry(convention_window, width=30)
    convention_name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(convention_window, text="Convention:  ").grid(row=1, column=0, padx=10, pady=10)
    convention_entry = tk.Entry(convention_window, width=60)
    convention_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(convention_window, text="Separator: ").grid(row=1, column=2, padx=10, pady=10, sticky='w')
    separator_entry = tk.Entry(convention_window, width=3)
    separator_entry.grid(row=1, column=3, padx=10, pady=10, sticky='e')

    save_convention_button = tk.Button(convention_window, text="Save", command=lambda: save_convention(convention_name_entry, convention_entry, separator_entry))
    save_convention_button.grid(row=2, column=3, padx=10, pady=10)

def create_project():
    create_window = tk.Toplevel(root)
    create_window.geometry('700x700')
    create_window.title("Create New Project")
    create_window.columnconfigure([0,1,2], weight=1, minsize=50)
    create_window.rowconfigure([0,1,2,3,4,5,6,8,9,10,11], weight=1)

    tk.Label(create_window, text="Project Name:").grid(row=0, column=0, padx=10, pady=10)
    project_name_entry = tk.Entry(create_window, width=50)
    project_name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(create_window, text="Save Location:").grid(row=1, column=0, padx=10, pady=10)
    folder_entry = tk.Entry(create_window, width=50)
    folder_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(create_window, text='Select a convention: ').grid(row=3, column=0, padx=10, pady=10)

    # Initialize the OptionMenu
    global convention_menu, selected_convention
    selected_convention = tk.StringVar(create_window)
    selected_convention.set('Select')  # Set default value
    convention_menu = tk.OptionMenu(create_window, selected_convention, '')
    convention_menu.config(width=50)
    convention_menu.grid(row=3, column=1, padx=10, pady=10)

    add_convention_button = tk.Button(create_window, text="Add a convention", command=add_naming_convention)
    add_convention_button.grid(row=3, column=2, padx=10, pady=10)

    
    display_convention_label = tk.Label(create_window, text='')
    display_convention_label.grid(row=4, column=0, padx=10, pady=10, columnspan=3)

    def on_option_change(*args):
        selected_value = selected_convention.get()
        if selected_value in data['convention']:
            conv = data['convention'][selected_value]['convention']
            sep = data['convention'][selected_value]['separator']
            display_convention_label.config(text=f"Selected convention: {conv}      separator: '{sep}'")
        else:
            display_convention_label.config(text='')

    selected_convention.trace("w", on_option_change)

    tk.Label(create_window, text="Path to TAPAS scripts: ").grid(row=5, column=0, padx=10, pady=10, sticky='w')
    tapas_path_entry = tk.Entry(create_window, width=50)
    tapas_path_entry.grid(row=5, column=1, padx=10, pady=10)
    tapas_path_entry.insert(0, tapas_path)

    browse_button = tk.Button(create_window, text="Browse", command=lambda: folder_entry.insert(0, filedialog.askdirectory(title="Select a Folder to Save Project")))
    browse_button.grid(row=1, column=2, padx=10, pady=10)

    def save_project():
        project_name = project_name_entry.get().strip()
        folder_path = folder_entry.get().strip()

        if not project_name:
            messagebox.showerror("Error", "Project name cannot be empty.")
            return

        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Please select a valid folder.")
            return

        # Create project folder
        project_path = os.path.join(folder_path, project_name)
        try:
            os.makedirs(project_path)
            messagebox.showinfo("Success", f"Project '{project_name}' created at: {project_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not create project folder: {e}")
        project_info = {
            "name": project_name,
            "date created":time.strftime("%A %d %B %Y %H:%M:%S"),
            "convention": {selected_convention.get():
                           {'convention': data['convention'][selected_convention.get()]['convention'], 'separator': data['convention'][selected_convention.get()]['separator']}
            },
            "tapas_path": tapas_path_entry.get(),
            "cellpose_model": cellpose_name_entry.get(),
            "image_channel": image_channel_entry.get(),
            "z_cropmin": z_cropmin_entry.get(),
            "z_cropmax": z_cropmax_entry.get(),
            "scale_x":scale_x_entry.get(),
            "scale_y":scale_y_entry.get(),

        }
        with open(os.path.join(project_path, f"{project_name}.yaml"), 'w') as file:
            yaml.dump(project_info, file, default_flow_style=False)
        initialise_project(tapas_path_entry.get(), image_channel_entry.get(), scale_x_entry.get(), scale_y_entry.get(),z_cropmin_entry.get(),z_cropmax_entry.get(), project_path, project_name+'extraction', cellpose_name_entry.get())
        #create_window.destroy()
    tk.Label(create_window, text="Cellpose model name: ").grid(row=6, column=0, padx=10, pady=10, sticky='w')
    cellpose_name_entry = tk.Entry(create_window, width=50)
    cellpose_name_entry.grid(row=6, column=1, padx=10, pady=10)
    cellpose_name_entry.insert(0, cellpose_model)

    frame = tk.Frame(master=create_window, relief=tk.RAISED, borderwidth=1)
    frame.grid(row=7, rowspan=4, columnspan=3)
    tk.Label(frame, text='Preprocessing').grid(row=7, column=1, padx=10, pady=10, sticky='w')
    tk.Label(frame, text='Channel to process: ').grid(row=8, column=0, padx=10, pady=10, sticky='w')
    image_channel_entry = tk.Entry(frame, width=10)
    image_channel_entry.grid(row=8, column=1, padx=10, pady=10, sticky='e')

    tk.Label(frame, text='Z crop: ').grid(row=9, column=0, padx=10, pady=10, sticky='w')
    z_cropmin_entry = tk.Entry(frame, width=10)
    z_cropmin_entry.grid(row=9, column=1, padx=10, pady=10, sticky='e')
    z_cropmin_entry.insert(0, 0)
    z_cropmax_entry = tk.Entry(frame, width=10)
    z_cropmax_entry.grid(row=9, column=2, padx=10, pady=10, sticky='e')
    z_cropmax_entry.insert(0, 18)

    tk.Label(frame, text='Scale XY ').grid(row=10, column=0, padx=10, pady=10, sticky='w')
    scale_x_entry = tk.Entry(frame, width=10)
    scale_x_entry.grid(row=10, column=1, padx=10, pady=10, sticky='e')
    scale_x_entry.insert(0, 1)
    scale_y_entry = tk.Entry(frame, width=10)
    scale_y_entry.grid(row=10, column=2, padx=10, pady=10, sticky='e')
    scale_y_entry.insert(0, 1)

    save_button = tk.Button(create_window, text="Create Project", command=save_project)
    save_button.grid(row=11, columnspan=3, pady=10)

    # Initial load of options
    refresh_options()

def load_project_data(filename="MarCell_data.yaml"):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
    return data

def load_options_from_yaml():
    """Load options from a YAML file."""
    with open('MarCell_data.yaml', 'r') as f:
        data = yaml.safe_load(f)
    return list(data['convention'].keys())

def update_option_menu(new_options):
    """Update the OptionMenu with new options."""
    # Clear the current options
    convention_menu['menu'].delete(0, 'end')
    for option in new_options:
        convention_menu['menu'].add_command(label=option, command=tk._setit(selected_convention, option))
    if new_options:
        selected_convention.set(new_options[0])  # Set default value

def refresh_options():
    """Refresh options from the YAML file."""
    new_options = load_options_from_yaml()
    update_option_menu(new_options)

# Initialize global data and path
global data
data = load_project_data(filename="MarCell_data.yaml")
tapas_path = data.get("tapas_path", "")
cellpose_model = data.get("cellpose_model", "")

# Create main window
root = tk.Tk()
root.title("Project Manager")

create_button = ttk.Button(root, text="Create Project", command=create_project)
create_button.pack(padx=20, pady=10)

open_button = ttk.Button(root, text="Open Project", command=open_project)
open_button.pack(padx=20, pady=10)

root.mainloop()