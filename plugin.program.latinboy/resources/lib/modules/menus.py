import sys
import json
import xbmc
import xbmcplugin
from .addonvar import addon_name
from .utils import add_dir
from .parser import Parser
from .dropbox import DownloadFile
from uservar import buildfile
from .addonvar import addon_icon, addon_fanart, local_string, build_file
from .colors import colors

HANDLE = int(sys.argv[1])
COLOR1 = colors.color_text1
COLOR2 = colors.color_text2

def main_menu():
    xbmcplugin.setPluginCategory(HANDLE, COLOR1('Menú Principal'))
    
    add_dir(COLOR1(f'{addon_name}'), '', '', addon_icon, addon_fanart, COLOR1(f'{addon_name}'), isFolder=False) 
    
    add_dir(COLOR2(local_string(30010)), '', 1, addon_icon, addon_fanart, COLOR2(local_string(30001)), isFolder=True)  # Build Menu
    
    add_dir(COLOR2(local_string(30011)), '', 5, addon_icon, addon_fanart, COLOR2(local_string(30002)), isFolder=True)  # Maintenance
    
    add_dir(COLOR2(local_string(30013)), '', 100, addon_icon, addon_fanart, COLOR2(local_string(30014)), isFolder=False)  # Notification
    
    add_dir(COLOR2(local_string(30015)), '', 9, addon_icon, addon_fanart, COLOR2(local_string(30016)), isFolder=False)  # Settings

def build_menu():
    xbmc.executebuiltin('Dialog.Close(busydialog)')
    xbmcplugin.setPluginCategory(HANDLE, local_string(30010))
    if buildfile.startswith('https://www.dropbox.com'):
        DownloadFile(buildfile, build_file)
        try:
            builds = json.load(open(build_file,'r')).get('builds')
        except:
            xml = Parser(build_file)
            builds = json.loads(xml.get_list2())['builds']
    elif not buildfile.endswith('.xml') and not buildfile.endswith('.json'):
        add_dir(local_string(30017),'','',addon_icon,addon_fanart,local_string(30017),isFolder=False)  # Invalid Build URL
        return
    else:
        p = Parser(buildfile)
        builds = json.loads(p.get_list())['builds']
    
    for build in builds:
        name = (build.get('name', local_string(30018)))  # Unknown Name
        version = (build.get('version', '0'))
        url = (build.get('url', ''))
        icon = (build.get('icon', addon_icon))
        fanart = (build.get('fanart', addon_fanart))
        description = (build.get('description', local_string(30019)))  # No Description Available.
        preview = (build.get('preview',None))
        
        if url.endswith('.xml') or url.endswith('.json'):
            add_dir(COLOR2(name),url,1,icon,fanart,COLOR2(description),name2=name,version=version,isFolder=True)
        add_dir(COLOR2(f'{name} {local_string(30020)} {version}'), url, 3, icon, fanart, description, name2=name, version=version, isFolder=False)  # Version
        if preview is not None:
            add_dir(COLOR1(local_string(30021) + ' ' + name + ' ' + local_string(30020) + ' ' + version), preview, 2, icon, fanart, COLOR2(description), name2=name, version=version, isFolder=False)  # Video Preview

def submenu_maintenance():
    kodi_ver = str(xbmc.getInfoLabel("System.BuildVersion")[:4])
    xbmcplugin.setPluginCategory(HANDLE, COLOR1(local_string(30022)))  # Maintenance
    add_dir(COLOR1('[B]Mantenimiento[/B]'),'','',addon_icon,addon_fanart, COLOR1('Menú de Mantenimiento'),isFolder=False)
    add_dir(COLOR2(local_string(30023)),'',6,addon_icon,addon_fanart,COLOR1(local_string(30005)),isFolder=False)  # Clear Packages
    add_dir(COLOR2(local_string(30024)),'',7,addon_icon,addon_fanart,COLOR2(local_string(30008)),isFolder=False)  # Clear Thumbnails
    add_dir(COLOR2(local_string(30012)), '', 4, addon_icon, addon_fanart, COLOR2(local_string(30003)), isFolder=False)  # Fresh Start
    if '20' in kodi_ver:
        add_dir(COLOR2(local_string(30025)),'',8,addon_icon,addon_fanart,COLOR2(local_string(30009)),isFolder=False)  # Advanced Settings K20
    if '21' in kodi_ver:
        add_dir(COLOR2(local_string(30106)),'',26,addon_icon,addon_fanart,COLOR2(local_string(30009)),isFolder=False)  # Advanced Settings K21
    add_dir(COLOR2(local_string(30064)),'',11,addon_icon,addon_fanart,COLOR2(local_string(30064)), isFolder=False)  # Edit Whitelist
    add_dir(COLOR2('Respaldar/Restaurar Build'),'',12,addon_icon,addon_fanart, COLOR2('Respaldar y restaurar tu Build de Kodi'))  # Backup Build
    add_dir(COLOR2('Respaldar/Restaurar Interfaz y Skin'),'',19,addon_icon,addon_fanart,COLOR2('Restaurar configuración de interfaz y Skin'))
    add_dir(COLOR2('Forzar Cierre'),'', 18, addon_icon,addon_fanart,COLOR2('Forzar el cierre de Kodi'))
    add_dir(COLOR2('Ver Registro'),'', 25, addon_icon,addon_fanart,COLOR2('Ver el registro de Kodi'), isFolder=False)

def backup_restore():
    xbmcplugin.setPluginCategory(HANDLE, COLOR1('Respaldar/Restaurar'))
    add_dir(COLOR1('[B]Respaldar/Restaurar[/B]'),'','',addon_icon,addon_fanart, COLOR1('Menú de Respaldo y Restauración'), isFolder=False)
    add_dir(COLOR2('Respaldar Build'),'',13,addon_icon,addon_fanart, COLOR2('Respaldar Build'), isFolder=False)  # Backup Build
    add_dir(COLOR2('Restaurar Respaldo'),'',14, addon_icon,addon_fanart, COLOR2('Restaurar Respaldo'))  # Restore Backup
    add_dir(COLOR2('Cambiar Carpeta de Respaldos'),'',16,addon_icon,addon_fanart, COLOR2('Cambia la ubicación donde se guardarán los respaldos.'), isFolder=False)  # Backup Location
    add_dir(COLOR2('Restablecer Carpeta de Respaldos'),'',17,addon_icon,addon_fanart, COLOR2('Restablece la ubicación de respaldos a su valor por defecto.'), isFolder=False)  # Reset Backup Location

def restore_gui_skin():
    add_dir(COLOR1('[B]Respaldar/Restaurar Interfaz y Skin[/B]'),'','',addon_icon,addon_fanart, COLOR1('Menú de Respaldo de Interfaz y Skin'), isFolder=False)
    add_dir(COLOR2('Respaldar Interfaz y Skin'),'',27,addon_icon,addon_fanart,COLOR2('Respaldar Interfaz y Skin'), isFolder=False)
    add_dir(COLOR2('Restaurar Configuración de Interfaz'),'',28, addon_icon,addon_fanart, COLOR2('Restaura tu configuración de interfaz.'), isFolder=False)
    add_dir(COLOR2('Restaurar Configuración del Skin'),'',29, addon_icon,addon_fanart, COLOR2('Restaura la configuración de tu Skin.'), isFolder=False)
    add_dir(COLOR2('Restaurar Interfaz por Defecto del Build'),'',20,addon_icon,addon_fanart,COLOR2('Restaurar Configuración de Interfaz'), isFolder=False)
    add_dir(COLOR2('Restaurar Skin por Defecto del Build'),'',21, addon_icon,addon_fanart, COLOR2('Restaurar Configuración del Skin'), isFolder=False)
