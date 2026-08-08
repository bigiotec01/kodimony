import xbmc
import xbmcgui
import xbmcaddon
import json
import base64
import xbmcvfs
import shutil
import xml.etree.ElementTree as ET
from .maintenance import clear_packages_startup
from .build_install import build_install
from uservar import buildfile, notify_url, addon_repo_url
from resources.lib.modules import addonvar
from .addonvar import setting, setting_set, addon_name, isBase64, headers, dialog, local_string, addon_id, addon_version

current_build = setting('buildname')
try:
    current_version = setting('buildversion') 
except:
    current_version = 0.0

class Startup:
    
    def seren_check(self):
        if '21' in str(xbmc.getInfoLabel("System.BuildVersion")[:4]) and xbmcvfs.exists(addonvar.seren):
            with open(addonvar.seren_glbs, encoding="utf8") as f:
                if addonvar.chk_glbs not in f.read():
                    try:
                        shutil.copyfile(addonvar.seren_fix, addonvar.seren_glbs)
                    except:
                        pass
        else:
            pass
            
    def check_updates(self):
           if current_build == 'No Build Installed':
               nobuild = dialog.yesnocustom(addon_name, 'Actualmente no tenés ningún Build instalado.\n¿Te gustaría instalar uno ahora?', 'Más tarde')
               if nobuild == 1:
                   xbmc.executebuiltin(f'ActivateWindow(10001, "plugin://{addon_id}/?mode=1",return)')
               elif nobuild == 0:
                   setting_set('buildname', 'No Build')
               else:
                   return
           try:
               xbmc.log(f"Valor de 'buildfile': {buildfile}", level=xbmc.LOGINFO) 
               response = self.get_page(buildfile)
               xbmc.log(f"Valor de 'respuesta del buildfile': {response}", level=xbmc.LOGINFO)
           except:
               return
           version = 0.0
           build_url = None
           try:
               try:
                   builds = json.loads(response)['builds']
               except json.JSONDecodeError as e:
                   xbmc.log(f"Error decodificando JSON: {e}", level=xbmc.LOGERROR)
                   xbmc.log(f"Respuesta recibida: {response}", level=xbmc.LOGERROR)
                   return
               for build in builds:
                       if build.get('name') == current_build:
                           version = str(build.get('version'))
                           build_url = build.get('url')
                           break
           except:
               builds = ET.fromstring(response)
               for tag in builds.findall('build'):
                       if tag.find('name').text == current_build:
                           version = str(tag.find('version').text)
                           build_url = tag.find('url').text
                           break
           # 3 decimal fix

           current_bump = 0
           version_bump = 0
           update = False
           version_display = str(version)

           try:
               current = str(current_version)
               version = str(version)
               c_splitted = current.split('.')
               v_splitted = version.split('.')
        
               if '.' in current:
                   current = float(f'{c_splitted[0]}.{c_splitted[1]}')
                   if len(c_splitted) == 3:
                       current_bump = int(c_splitted[2])
               if '.' in version:
                   version = float(f'{v_splitted[0]}.{v_splitted[1]}')
                   if len(v_splitted) == 3:
                       version_bump = int(v_splitted[2])
               if float(version) > float(current):
                   update = True
               elif float(version) == float(current) and version_bump > current_bump:
                   update = True
               else:
                   update = False
           
           except ValueError as e:
               print(f'Invalid Version Number. It must be numeric and no more than 3 decimals. Error Details - {e}')
               update = False
           
           if update and setting('update_passed') != 'true' and setting('update_dismissed_version') != version_display:
               if not build_url:
                   xbmc.log(f"No se encontro 'url' para el build '{current_build}' en {buildfile}", level=xbmc.LOGERROR)
                   return
               update_available = xbmcgui.Dialog().yesnocustom(addon_name, local_string(30047) + ' ' + current_build +' ' + local_string(30048) + '\n' + local_string(30049) + ' ' + str(current_version) + '\n' + local_string(30050) + ' ' + version_display + '\n' + local_string(30051), 'Remind Later')
               if update_available == 1:
                   build_install(current_build, current_build, version_display, build_url, confirm=False)
               elif update_available == 0:
                   setting_set('update_dismissed_version', version_display)
               else:
                   return
           else:
               return

    @staticmethod
    def _version_tuple(v):
        parts = []
        for p in str(v).split('.'):
            digits = ''.join(ch for ch in p if ch.isdigit())
            parts.append(int(digits) if digits else 0)
        return tuple(parts)

    def addon_update_check(self):
        try:
            response = self.get_page(addon_repo_url)
            tree = ET.fromstring(response)
        except:
            return
        remote_version = None
        for tag in tree.findall('addon'):
            if tag.get('id') == addon_id:
                remote_version = tag.get('version')
                break
        if not remote_version or setting('addon_update_dismissed_version') == remote_version:
            return
        try:
            is_newer = self._version_tuple(remote_version) > self._version_tuple(addon_version)
        except ValueError:
            return
        if not is_newer:
            return
        update_available = xbmcgui.Dialog().yesnocustom(addon_name, local_string(30047) + ' ' + addon_name + ' ' + local_string(30048) + '\n' + local_string(30049) + ' ' + str(addon_version) + '\n' + local_string(30050) + ' ' + str(remote_version) + '\n' + local_string(30051), 'Remind Later')
        if update_available == 1:
            xbmc.executebuiltin('UpdateAddonRepos')
            xbmc.sleep(2000)
            xbmc.executebuiltin(f'InstallAddon({addon_id})')
        elif update_available == 0:
            setting_set('addon_update_dismissed_version', remote_version)

    def file_check(self, bfile):
        if isBase64(bfile):
            return base64.b64decode(bfile).decode('utf8')
        else:
            return bfile
            
    def get_page(self, url):
           from urllib.request import Request,urlopen
           req = Request(self.file_check(url), headers = headers)
           return urlopen(req).read()
        
    def save_menu(self):
        save_items = []
        choices = ["Trakt & Debrid", "Claves de API de YouTube", "Favoritos", "Configuración Avanzada", "Fuentes"]
        save_select = dialog.multiselect(addon_name + ' - ' + local_string(30052),choices, preselect=[])  # Select Save Items
        if save_select == None:
            return
        else:
            for index in save_select:
                save_items.append(choices[index])

        if 'Trakt & Debrid' in save_items:
            setting_set('savedata','true')
        else:
            setting_set('savedata','false')

        if 'Claves de API de YouTube' in save_items:
            setting_set('saveyoutube','true')
        else:
            setting_set('saveyoutube','false')

        if 'Favoritos' in save_items:
            setting_set('savefavs','true')
        else:
            setting_set('savefavs','false')

        if 'Configuración Avanzada' in save_items:
            setting_set('saveadvanced','true')
        else:
            setting_set('saveadvanced','false')

        if 'Fuentes' in save_items:
            setting_set('savesources', 'true')
        else:
            setting_set('savesources', 'false')
  
        setting_set('firstrunSave', 'true')

    def notify_check(self):
        from ..GUIcontrol import notify
        info = notify.get_notify()
        current_notify = int(setting('notifyversion'))
        notify_version = info[0]
        message = info[1]
        if not setting('firstrunNotify')=='true' or notify_version > current_notify:
            notify.notification(message)
            setting_set('firstrunNotify', 'true')
            setting_set('notifyversion', str(notify_version))    

    def run_startup(self):
        self.seren_check()
        if setting('firstrun') == 'true':
            if current_build == 'Xlite Switch':
                from .save_data import backup_gui_skin
                xbmc.executebuiltin('UpdateAddonRepos')
                xbmc.sleep(2000)
                xbmc.executebuiltin('UpdateLocalAddons')
                backup_gui_skin()
                setting_set('firstrun', 'false')
            else:
                from resources.lib.modules.addons_enable import enable_addons
                from .save_data import backup_gui_skin
                enable_addons()
                backup_gui_skin()
                setting_set('firstrun', 'false')
        else:
            if setting('autoclearpackages')=='true':
                clear_packages_startup()
            xbmc.sleep(2000)
            self.notify_check()
            xbmc.sleep(3000)      #Delay Build Update Notification
            self.check_updates()
            xbmc.sleep(1000)      #Delay Addon Update Notification
            self.addon_update_check()
            
