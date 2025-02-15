import xbmc
import xbmcgui
import xbmcvfs	
import xbmcaddon
import os
import shutil
import json
import xml.etree.ElementTree as ET 
from .addonvar import user_path, data_path, setting, addon_id, packages, addon_name, dialog, addon_icon

user_path = xbmcvfs.translatePath('special://userdata/')	
data_path = os.path.join(user_path, 'addon_data/')
skin_path = xbmcvfs.translatePath('special://skin/')
text_path = os.path.join(xbmcvfs.translatePath(xbmcaddon.Addon().getAddonInfo('path')), 'resources/', 'texts/')
skin = ET.parse(os.path.join(skin_path, 'addon.xml'))
root = skin.getroot()
skin_id = root.attrib['id']
gui_save = os.path.join(user_path, 'gui_settings/')
gui_save_user = os.path.join(user_path, 'gui_settings_user/')
gui_file = 'guisettings.xml'
skinsc = 'script.skinshortcuts'

def backup(path, file):
    if os.path.exists(os.path.join(path, file)):
        try:
            if os.path.isfile(os.path.join(path, file)):
                xbmcvfs.copy(os.path.join(path, file), os.path.join(packages, file))   #Backup your Kodi specifics (advancedsettings, favs etc...)
            elif os.path.isdir(os.path.join(path, file)):
                shutil.copytree(os.path.join(path, file), os.path.join(packages, file), dirs_exist_ok=True)   #Backup your Trakt & Debrid data
        except Exception as e:
            xbmc.log('Failed to backup %s. Reason: %s' % (os.path.join(packages, file), e), xbmc.LOGINFO)

def backup_gui_skin():
    if not os.path.exists(gui_save):
        os.mkdir(gui_save)
    if os.path.exists(os.path.join(user_path, gui_file)) and os.path.exists(os.path.join(gui_save)):
        try:
            xbmcvfs.copy(os.path.join(user_path, gui_file), os.path.join(gui_save, gui_file))   #Backup gui settings
        except Exception as e:
            xbmc.log('Failed to backup %s. Reason: %s' % (os.path.join(gui_save, gui_file), e), xbmc.LOGINFO)     
    if os.path.exists(os.path.join(data_path, skin_id)) and os.path.exists(os.path.join(gui_save)):
        try:
            shutil.copytree(os.path.join(data_path, skin_id), os.path.join(gui_save, skin_id), dirs_exist_ok=True)   #Backup skin settings
        except Exception as e:
                xbmc.log('Failed to backup %s. Reason: %s' % (os.path.join(gui_save, skin_id), e), xbmc.LOGINFO)
    if os.path.exists(os.path.join(data_path, skinsc)) and os.path.exists(os.path.join(gui_save)):
        try:
            shutil.copytree(os.path.join(data_path, skinsc), os.path.join(gui_save, skinsc), dirs_exist_ok=True)   #Backup skinshortcut settings
        except Exception as e:
            xbmc.log('Failed to backup %s. Reason: %s' % (os.path.join(gui_save, skinsc), e), xbmc.LOGINFO)

def backup_gui_skin_user():
    if not os.path.exists(gui_save_user):
        os.mkdir(gui_save_user)
    if os.path.exists(os.path.join(user_path, gui_file)) and os.path.exists(os.path.join(gui_save_user)):
        try:
            xbmcvfs.copy(os.path.join(user_path, gui_file), os.path.join(gui_save_user, gui_file))   #Backup gui settings
        except Exception as e:
            xbmc.log('Failed to backup %s. Reason: %s' % (os.path.join(gui_save_user, gui_file), e), xbmc.LOGINFO)     
    if os.path.exists(os.path.join(data_path, skin_id)) and os.path.exists(os.path.join(gui_save_user)):
        try:
            shutil.copytree(os.path.join(data_path, skin_id), os.path.join(gui_save_user, skin_id), dirs_exist_ok=True)   #Backup skin settings
        except Exception as e:
                xbmc.log('Failed to backup %s. Reason: %s' % (os.path.join(gui_save_user, skin_id), e), xbmc.LOGINFO)
    if os.path.exists(os.path.join(data_path, skinsc)) and os.path.exists(os.path.join(gui_save_user)):
        try:
            shutil.copytree(os.path.join(data_path, skinsc), os.path.join(gui_save_user, skinsc), dirs_exist_ok=True)   #Backup skinshortcut settings
        except Exception as e:
            xbmc.log('Failed to backup %s. Reason: %s' % (os.path.join(gui_save_user, skinsc), e), xbmc.LOGINFO)
    xbmcgui.Dialog().notification(addon_name, 'Backup Complete!', addon_icon, 6000)
           
def restore(path, file):
    if os.path.exists(os.path.join(packages, file)):
        try:
            if os.path.isfile(os.path.join(packages, file)):
                if os.path.exists(os.path.join(user_path, file)):
                    os.unlink(os.path.join(path, file))   #Remove Kodi specifics (advancedsettings, favs etc...) included with new install
                shutil.move(os.path.join(packages, file), os.path.join(path, file))   #Restore your backed up Kodi specifics (advancedsettings, favs etc...)
            elif os.path.isdir(os.path.join(packages, file)):
                shutil.copytree(os.path.join(packages, file), os.path.join(path, file), dirs_exist_ok=True)   #Restore your backed up Trakt & Debrid data
        except Exception as e:
            xbmc.log('Failed to restore %s. Reason: %s' % (os.path.join(path, file), e), xbmc.LOGINFO)

def restore_gui():
    if os.path.exists(os.path.join(gui_save, gui_file)):
        try:
            xbmcvfs.copy(os.path.join(gui_save, gui_file), os.path.join(user_path, gui_file))   #Restore your backed up gui settings
        except Exception as e:
            xbmc.log('Failed to restore %s. Reason: %s' % (os.path.join(user_path, gui_file), e), xbmc.LOGINFO)
    dialog.ok(addon_name, 'To save changes you now need to force close Kodi, Press OK to force close Kodi')
    os._exit(1)
    
def restore_skin():
    if os.path.exists(os.path.join(data_path, skin_id)):
        try:
            shutil.copytree(os.path.join(gui_save, skin_id), os.path.join(data_path, skin_id), dirs_exist_ok=True)   #Restore your backed up skin settings
        except Exception as e:
            xbmc.log('Failed to restore %s. Reason: %s' % (os.path.join(data_path, skin_id), e), xbmc.LOGINFO)
    if os.path.exists(os.path.join(data_path, skinsc)) and os.path.exists(os.path.join(gui_save, skinsc)):
        try:
            shutil.copytree(os.path.join(gui_save, skinsc), os.path.join(data_path, skinsc), dirs_exist_ok=True)   #Restore your backed up skinshortcuts settings
        except Exception as e:
            xbmc.log('Failed to restore %s. Reason: %s' % (os.path.join(data_path, skinsc), e), xbmc.LOGINFO)
    dialog.ok(addon_name, 'To save changes you now need to force close Kodi, Press OK to force close Kodi')
    os._exit(1)

def restore_gui_user():
    if os.path.exists(os.path.join(gui_save_user, gui_file)):
        try:
            xbmcvfs.copy(os.path.join(gui_save_user, gui_file), os.path.join(user_path, gui_file))   #Restore your backed up gui settings
        except Exception as e:
            xbmc.log('Failed to restore %s. Reason: %s' % (os.path.join(user_path, gui_file), e), xbmc.LOGINFO)
    dialog.ok(addon_name, 'To save changes you now need to force close Kodi, Press OK to force close Kodi')
    os._exit(1)
    
def restore_skin_user():
    if os.path.exists(os.path.join(data_path, skin_id)):
        try:
            shutil.copytree(os.path.join(gui_save_user, skin_id), os.path.join(data_path, skin_id), dirs_exist_ok=True)   #Restore your backed up skin settings
        except Exception as e:
            xbmc.log('Failed to restore %s. Reason: %s' % (os.path.join(data_path, skin_id), e), xbmc.LOGINFO)
    if os.path.exists(os.path.join(data_path, skinsc)) and os.path.exists(os.path.join(gui_save_user, skinsc)):
        try:
            shutil.copytree(os.path.join(gui_save_user, skinsc), os.path.join(data_path, skinsc), dirs_exist_ok=True)   #Restore your backed up skinshortcuts settings
        except Exception as e:
            xbmc.log('Failed to restore %s. Reason: %s' % (os.path.join(data_path, skinsc), e), xbmc.LOGINFO)
    dialog.ok(addon_name, 'To save changes you now need to force close Kodi, Press OK to force close Kodi')
    os._exit(1)

def save_backup_restore(_type: str) -> None:
    config_file = os.path.join(text_path, 'backup_restore.json')
    
    if not os.path.exists(config_file):
        xbmc.log(f'[ERROR][SAVE] Archivo de configuración no encontrado: {config_file}', xbmc.LOGINFO)
        return

    xbmc.log(f'[DEBUG][SAVE] Iniciando proceso: {_type}', xbmc.LOGINFO)
    xbmc.log(f'[DEBUG][SAVE] Usando archivo de configuración: {config_file}', xbmc.LOGINFO)

    try:
        with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
            item_list = json.loads(f.read())
            xbmc.log(f'[DEBUG][SAVE] Configuración cargada: {len(item_list.keys())} ítems', xbmc.LOGINFO)
    except Exception as e:
        xbmc.log(f'[ERROR][SAVE] Fallo al cargar JSON: {str(e)}', xbmc.LOGINFO)
        return

    for item in item_list.keys():
        xbmc.log(f'[DEBUG][SAVE] Procesando ítem: {item}', xbmc.LOGINFO)
        
        try:
            setting_id = item_list[item]['setting']
            original_path = item_list[item]['path']
            xbmc.log(f'[DEBUG][SAVE] Setting ID: {setting_id} | Path original: {original_path}', xbmc.LOGINFO)

            # Resolver rutas dinámicas
            if original_path == 'user_path':
                final_path = user_path
            elif original_path == 'data_path':
                final_path = data_path
            else:
                final_path = original_path
                
            xbmc.log(f'[DEBUG][SAVE] Ruta final resuelta: {final_path}', xbmc.LOGINFO)

            # Verificar si el setting está habilitado
            setting_value = setting(setting_id)
            xbmc.log(f'[DEBUG][SAVE] Valor del setting {setting_id}: {setting_value}', xbmc.LOGINFO)
            
            if setting_value != 'true':
                xbmc.log(f'[DEBUG][SAVE] Saltando ítem {item} - Setting deshabilitado', xbmc.LOGINFO)
                continue

            # Definir archivos a procesar
            files_to_process = [
                ('settings.xml', os.path.join(final_path, item, 'settings.xml')),
                ('rdauth.json', os.path.join(final_path, item, 'rdauth.json')),
                ('api_keys.json', os.path.join(final_path, item, 'api_keys.json'))
            ]

            if _type == 'backup':
                xbmc.log(f'[DEBUG][SAVE] Iniciando BACKUP para: {item}', xbmc.LOGINFO)
                for file_type, source_path in files_to_process:
                    if os.path.exists(source_path):
                        xbmc.log(f'[DEBUG][BACKUP] Copiando {file_type}: {source_path}', xbmc.LOGINFO)
                        # Aquí debería ir tu lógica real de backup
                        # backup(final_path, os.path.join(item, file_type))
                    else:
                        xbmc.log(f'[WARNING][BACKUP] Archivo no existe: {source_path}', xbmc.LOGINFO)

                # Backup especial para Kodi
                kodi_specific_path = os.path.join(user_path, item)
                if os.path.exists(kodi_specific_path):
                    xbmc.log(f'[DEBUG][BACKUP] Copiando datos Kodi: {kodi_specific_path}', xbmc.LOGINFO)
                    # backup(user_path, item)
                else:
                    xbmc.log(f'[WARNING][BACKUP] Ruta Kodi no existe: {kodi_specific_path}', xbmc.LOGINFO)

            elif _type == 'restore':
                xbmc.log(f'[DEBUG][SAVE] Iniciando RESTORE para: {item}', xbmc.LOGINFO)
                for file_type, target_path in files_to_process:
                    # Aquí debería ir tu lógica real de restore
                    # restore(final_path, os.path.join(item, file_type))
                    xbmc.log(f'[DEBUG][RESTORE] Restaurando {file_type} a: {target_path}', xbmc.LOGINFO)

                # Restore especial para Kodi
                kodi_restore_path = os.path.join(user_path, item)
                xbmc.log(f'[DEBUG][RESTORE] Restaurando datos Kodi a: {kodi_restore_path}', xbmc.LOGINFO)
                # restore(user_path, item)

        except KeyError as e:
            xbmc.log(f'[ERROR][SAVE] KeyError en ítem {item}: {str(e)}', xbmc.LOGINFO)
        except Exception as e:
            xbmc.log(f'[ERROR][SAVE] Error general en ítem {item}: {str(e)}', xbmc.LOGINFO)
            import traceback
            xbmc.log(f'[TRACEBACK][SAVE] {traceback.format_exc()}', xbmc.LOGINFO)

    xbmc.log(f'[DEBUG][SAVE] Proceso {_type} completado', xbmc.LOGINFO)
