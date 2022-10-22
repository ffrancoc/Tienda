pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'tienda')
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'gtk/help-overlay.blp',
    'gtk/login.blp',
    'gtk/window.blp',
    'gtk/home-view.blp',
    'gtk/user-view.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)


gnome.compile_resources('tienda',
  'tienda.gresource.xml',
  dependencies: blueprints,
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'tienda.in',
  output: 'tienda',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

tienda_sources = [
  '__init__.py',
  'main.py',
  'db/database.py',
  'widgets/dialogs.py',
  'view/login.py',
  'view/window.py',
  'view/home.py',
  'view/user.py',
]

install_data(tienda_sources, install_dir: moduledir)
