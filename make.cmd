python make_properties.py
pyinstaller ^
  --onefile ^
  --noconsole ^
  --noupx ^
  --win-private-assemblies ^
  --icon=.\icon.ico ^
  --noconfirm ^
  --version-file=properties.rc ^
  fetique.py
pause