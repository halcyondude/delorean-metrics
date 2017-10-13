Check out http://smashing.github.io/ for more information.

installation directions (Fedora)
--------------------------------

- https://github.com/Smashing/smashing

```
sudo dnf groupinstall 'Development Tools'
sudo dnf install ruby ruby-devel rubygem-json nodejs gcc-c++
gem install --user-install bundler
gem install --user-install smashing
```

now you can make a new boilerplate dashboard with:

```
smashing new my-dashboard-name
```

or you can bundle up the existing dlrnapi-dashboard board with...

```
cd dlrnapi-dashboard
bundle
smashing start
```
