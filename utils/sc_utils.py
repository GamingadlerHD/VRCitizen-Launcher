from tkinter import messagebox
import os
import shutil
from utils.vorpX_utils import PrepareVorpX
from utils.xml_editor import update_vr_settings_from_xml_to_xml, update_xml_by_dict
from utilities import is_admin, is_process_running, modify_hosts, backup_file, launch_process, wait_for_process, wait_for_exit, kill_process_by_name
from validation import fits_on_any_monitor
from i18n import translate
from constants import HOSTS_FILE, DXGI_DLL, EASY_ANTICHEAT_FOLDER
from logs import log, warn, error

async def Launch(ui_elements, launcher_settings, vorpx_settings):
    sc_folder_path = ui_elements['sc_entry'].get()
    vorpx_path = ui_elements['vorpx_entry'].get()
    launcher_path = ui_elements['launcher_entry'].get()
    stay_in_vr = ui_elements['stay_in_vr'].get()
    additional_popups = ui_elements['additional_popup'].get()
    use_dxgi = bool(ui_elements['use_dxgi'].get())

    log("Launch parameters:")
    log(f"  SC Folder: {sc_folder_path}")
    log(f"  VorpX Path: {vorpx_path}")
    log(f"  Launcher Path: {launcher_path}")
    log(f"  Stay in VR: {stay_in_vr}")
    log(f"  Additional Popups: {additional_popups}")
    log(f"  Use DXGI: {use_dxgi}")

    # Derived paths
    eac_folder_path = EASY_ANTICHEAT_FOLDER
    attr_orig_path = os.path.join(sc_folder_path, "user/client/0/Profiles/default/attributes.xml")
    sc_executable = os.path.join(sc_folder_path, "Bin64/StarCitizen.exe")
    dxgi_dest_path = os.path.join(sc_folder_path, DXGI_DLL)

    # Pre-Validation
    script_dir = os.getcwd()
    dxgi_path = os.path.join(script_dir, "dxgi.dll")

    if not all([sc_folder_path, vorpx_path]):
        messagebox.showerror(
            translate("error_title"), 
            translate("select_all_files")
        )
        return

    # Path validations
    if use_dxgi is True and bool(os.path.isfile(dxgi_path)) is False and bool(os.path.isfile(dxgi_dest_path)) is False:
        messagebox.showerror(
            translate("error_title"), 
            translate("hook_file_not_found").format(dxgi_path=dxgi_path)
        )
        return

    if not os.path.isdir(os.path.join(sc_folder_path, "user/client/0/")):
        error(f"Star Citizen user folder not found: {os.path.join(sc_folder_path, 'user/client/0/')}")
        messagebox.showerror(
            translate("error_title"), 
            translate("no_user_folder")
        )
        return

    if not os.path.isdir(sc_folder_path):
        error(f"Star Citizen folder not found: {sc_folder_path}")
        messagebox.showerror(
            translate("error_title"), 
            translate("sc_folder_not_found").format(sc_folder_path=sc_folder_path)
        )
        return
    
    if not os.path.isfile(vorpx_path):
        error(f"VorpX executable not found: {vorpx_path}")
        messagebox.showerror(
            translate("error_title"), 
            translate("vorpx_exe_not_found").format(vorpx_path=vorpx_path)
        )
        return 
    
    if not os.path.isfile(sc_executable):
        error(f"Star Citizen executable not found: {sc_executable}")
        messagebox.showerror(
            translate("error_title"), 
            translate("sc_exe_not_found").format(sc_executable=sc_executable)
        )
        return
    
    if not os.path.isfile(attr_orig_path):
        error(f"Attributes file not found: {attr_orig_path}")
        messagebox.showerror(
            translate("error_title"), 
            translate("attributes_file_not_found").format(attr_orig_path=attr_orig_path)
        )
        return

    if not is_admin():
        error("Administrator privileges required but not available")
        messagebox.showerror(
            translate("admin_required_title"), 
            translate("admin_required_message")
        )
        return
    
    log("All path validations passed successfully")
    
    # Resolution validation
    width = int(ui_elements['width_entry'].get())
    height = int(ui_elements['height_entry'].get())
    
    if not fits_on_any_monitor(width, height):
        if not ui_elements['ign_res_warning'].get():
            warn(f"Resolution {width}x{height} does not fit on any monitor")
            messagebox.showerror(
                translate("error_title"), 
                translate("resolution_too_small")
            )
            return
        warn(f"Resolution {width}x{height} warning ignored by user")
    else:
        log("Resolution compatibility check passed")
    
    log("Starting main launch sequence...")
    
    try:
        doneStepID = 0
        # 1 = modify hosts file
        # 2 = paste dxgi.dll
        # 3 = start vorpX
        # 4 = update attributes file
        # 5 = delete EAC folder
        # 6 = start RSI Launcher

        sc_proc_name = os.path.basename(sc_executable)
        vorpx_proc_name = os.path.basename(vorpx_path)
    
        try:
            if (additional_popups):
                messagebox.showinfo(translate("info_title"), translate("modifying_hosts"))
            backup_file(HOSTS_FILE)
            modify_hosts(add=True)
            doneStepID += 1

            # Step 2: Apply DXGI hook if needed
            if (use_dxgi is True):
                if (additional_popups):
                    messagebox.showinfo(
                        translate("info_title"), 
                        translate("pasting_dxgi")
                    )
                apply_hook_helper(dxgi_dest_path, Add=True)
                doneStepID += 1
            
            # Step 3: Prepare VorpX
            keepKeybinds = vorpx_settings['keep_keybinds'].get()
            template_name = ui_elements['template_dropdown'].get()
            custom_config = vorpx_settings["custom_config"].get()
            
            log(f"VorpX settings - Template: {template_name}, Custom Config: {custom_config}, Keep Keybinds: {keepKeybinds}")
            await PrepareVorpX(vorpx_path, template_name, custom_config, keepKeybinds)

            # Start VorpX if not running
            if not is_process_running(vorpx_proc_name):
                if (additional_popups):
                    messagebox.showinfo(
                        translate("info_title"), 
                        translate("vorpx_start")
                    )
                launch_process(vorpx_path)
                log("VorpX launched successfully")
            else:
                log(f"VorpX already running: {vorpx_proc_name}")
            doneStepID += 1

            # Step 4: Update attributes file
            backup_file(attr_orig_path)
            
            # Update view attributes
            view_attr = {
                'Width': ui_elements['width_entry'].get(), 
                'Height': ui_elements['height_entry'].get(), 
                'FOV': ui_elements['fov_entry'].get()
            }
            log(f"View attributes: {view_attr}")
            doneStepID += 1
            update_xml_by_dict(attr_orig_path, view_attr)

            # Update launcher settings
            stVal = {}
            for component_name, component_value in launcher_settings.items():
                stVal[component_name] = component_value.get()
            log(f"Launcher settings: {stVal}")
            update_xml_by_dict(attr_orig_path, stVal)

            # Wait for VorpX to be ready
            log("Waiting for VorpX to be fully started")
            if (additional_popups):
                messagebox.showinfo(
                    translate("info_title"), 
                    translate("waiting_vorpx_start")
                )
            await wait_for_process(vorpx_proc_name)
            log("VorpX is now running and ready")

            if (additional_popups):
                messagebox.showinfo(
                    translate("info_title"), 
                    translate("deleting_eac")
                )
        
            if not os.path.isdir(eac_folder_path):
                log("EAC folder does not exist - already removed or not present")
                if (additional_popups):
                    messagebox.showinfo(
                        translate("info_title"), 
                        translate("eac_already_removed")
                    )
            else:
                log(f"Removing EAC folder: {eac_folder_path}")
                try:
                    shutil.rmtree(eac_folder_path, ignore_errors=True)
                    log("EAC folder removed successfully")
                    if (additional_popups):
                        messagebox.showinfo(translate("info_title"), translate("eac_removed"))
                except Exception as e:
                    warn(f"Failed to remove EAC folder: {e}")
            doneStepID += 1
            
            launch_process(launcher_path)
            if (additional_popups):
                messagebox.showinfo(
                    translate("info_title"), 
                    translate("waiting_launcher_start")
                )

            # Monitor Star Citizen if staying in VR
            if (stay_in_vr):
                await wait_for_process("StarCitizen.exe")
                log("Star Citizen process detected")
                
                if (additional_popups):
                    messagebox.showinfo(
                        translate("info_title"), 
                        translate("waiting_sc_start")
                    )

                log("Waiting for Star Citizen to exit...")
                await wait_for_exit(sc_proc_name)
                log("Star Citizen has exited, initiating cleanup")
                quit_vr_mode(vorpx_proc_name, dxgi_dest_path, attr_orig_path, additional_popups, doneStepID)
            else:
                log("Stay in VR mode disabled - launch sequence complete")
                
            log("=== Launch sequence completed successfully ===")

        except Exception as e:
            error(f"Error during launch sequence: {e}")
            messagebox.showerror(
                translate("error_title"), 
                translate("error_occurred_revert").format(e=e)
            )
            quit_vr_mode(vorpx_proc_name, dxgi_dest_path, attr_orig_path, additional_popups, doneStepID)

    except Exception as e:
        error(f"Critical error in launch operation: {e}")
        messagebox.showerror(
            translate("error_title"), 
            translate("operation_failed").format(e=e)
        )
        log("Launch operation failed with critical error")

def quit_vr_mode(vorpx_proc_name, dxgi_dest_path, attr_orig_path, additional_popups, doneStepID):
    try:
        if doneStepID > 0:
            if additional_popups:
                messagebox.showinfo(translate("info_title"), translate("restoring_hosts"))
            modify_hosts(add=False)
            if os.path.exists(HOSTS_FILE + ".backup"):
                os.remove(HOSTS_FILE + ".backup")
                log("Hosts file backup removed")

        if doneStepID > 1:
            if additional_popups:
                messagebox.showinfo(translate("info_title"), translate("removing_dxgi"))
            apply_hook_helper(dxgi_dest_path, Add=False)

        if doneStepID > 2:
            if additional_popups:
                messagebox.showinfo(translate("info_title"), translate("killing_vorpx"))
            kill_process_by_name(vorpx_proc_name)

        if doneStepID > 3:
            if additional_popups:
                messagebox.showinfo(translate("info_title"), translate("restoring_attributes"))
            if os.path.exists(attr_orig_path + ".backup"):
                update_vr_settings_from_xml_to_xml(
                    attr_orig_path + ".backup", attr_orig_path)
                os.remove(attr_orig_path + ".backup")

        messagebox.showinfo(
            translate("restored_title"), 
            translate("restored_message")
        )

    except Exception as e:
        error(f"Error during VR mode cleanup: {e}")
        messagebox.showerror(
            translate("error_title"), 
            translate("error_quitting_vr").format(e=e)
        )

def apply_hook_helper(destPath, Add=True):
    action = "Add" if Add else "Remove"
    local = os.path.join(os.getcwd(), "dxgi.dll")
    if not os.path.isfile(local) and not os.path.isfile(destPath): 
        warn("Neither local nor destination DXGI file exists")
        return
        
    try:
        if Add:
            if os.path.isfile(local) and not os.path.isfile(destPath):
                shutil.copy2(local, destPath)
                log(f"DXGI hook copied successfully from {local} to {destPath}")
            elif os.path.isfile(destPath):
                log("DXGI hook already exists at destination")
            else:
                warn("Local DXGI file not found, cannot add hook")
        elif not Add:
            if os.path.isfile(destPath):
                if not os.path.isfile(local):
                    log("Backing up DXGI hook to local directory")
                    shutil.copy2(destPath, local)
                os.remove(destPath)
                log(f"DXGI hook removed successfully from {destPath}")
            else:
                log("DXGI hook not found at destination - nothing to remove")
    except Exception as e:
        error(f"Failed to {action.lower()} DXGI hook: {e}")
        raise
    