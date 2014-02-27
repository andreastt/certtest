# Run with `source setup_environment.sh`

echo "Setting up virtualenv"
which pip
if [ $? != 0 ]; then
  which easy_install
  if [ $? != 0 ]; then
    echo "You need to have easy_install on your path"
    exit 0
  fi
  easy_install pip
fi
if [ ! -d "cert_venv" ]; then
  pip install virtualenv
  virtualenv --no-site-packages cert_venv
fi
source cert_venv/bin/activate
pip install marionette_client
pip install tornado
echo "Installing CertTest app on phone"
pushd device_setup
python device_setup.py
popd
echo "Done"
