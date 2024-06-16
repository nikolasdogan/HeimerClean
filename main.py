import os

import tray_icon
from helper.log_helper import log
from helper.regedit_helper import create_regedit_entry, read_regedit_entry
from helper.restart_helper import restart
from helper.settings_helper import check_settings_ini
from helper.update_helper import check_for_updates, apply_update


def main():
    # %LOCALAPPDATA% değişkenini kullanarak first_run_marker dosyasının yolunu belirleyin
    local_app_data = os.getenv('LOCALAPPDATA')
    first_run_marker = os.path.join(local_app_data, "HeimerClean", "FirstRun.marker")

    if not os.path.exists(first_run_marker):
        if check_settings_ini():
            # İşaret dosyasını oluştur
            with open(first_run_marker, 'w') as f:
                f.write('')
            if read_regedit_entry() is None:
                create_regedit_entry()
            # Uygulamayı yeniden başlat
            log("Application for Reboot", level="WARNING")
            restart()
            return

    # Güncelleme kontrolü yap
    # log("Uygulama başlatıldı. Güncelleme kontrolü yapılıyor...", level="INFO")
    print("Uygulama başlatıldı. Güncelleme kontrolü yapılıyor...")
    release_info = check_for_updates()
    if release_info:
        log(f"Yeni bir sürüm bulundu: {release_info['tag_name']}. Güncelleme uygulanıyor...", level="INFO")
        print(f"Yeni bir sürüm bulundu: {release_info['tag_name']}. Güncelleme uygulanıyor...")
        apply_update(release_info)
    else:
        # log("Güncel sürüm kullanılıyor.", level="INFO")
        print("Güncel sürüm kullanılıyor.")

    # settings.ini kontrolünden sonra tray iconu kur
    # Tray icon kurulum fonksiyonunu buraya ekleyin
    icon = tray_icon.main()


if __name__ == "__main__":
    main()
