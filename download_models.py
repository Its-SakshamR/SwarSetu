import argostranslate.package

print("Updating package index...")
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()

# Target language codes: 'hi' for Hindi, 'bn' for Bengali, 'ur' for Urdu
for lang in ['hi', 'bn', 'ur']:
    print(f"Locating English -> {lang} package...")
    package_to_install = next(
        filter(
            lambda x: x.from_code == 'en' and x.to_code == lang, available_packages
        ), None
    )
    if package_to_install:
        print(f"Downloading and installing English -> {lang}...")
        argostranslate.package.install_from_path(package_to_install.download())
        print(f"Success!")
    else:
        print(f"Could not find package for English -> {lang}.")
        
    print(f"Locating {lang} -> English package...")
    package_to_install = next(
        filter(
            lambda x: x.from_code == lang and x.to_code == 'en', available_packages
        ), None
    )
    if package_to_install:
        print(f"Downloading and installing {lang} -> English...")
        argostranslate.package.install_from_path(package_to_install.download())
        print(f"Success!")
    else:
        print(f"Could not find package for {lang} -> English.")