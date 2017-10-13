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
```

The output should look like this:

```
[you@yourbox dlrnapi-dashboard] $ bundle
Fetching https://github.com/halcyondude/ruby_dlrnapi.git
Fetching gem metadata from https://rubygems.org/...........
Fetching gem metadata from https://rubygems.org/...
Fetching gem metadata from https://rubygems.org/..
Resolving dependencies...
Using backports 3.8.0
Using bundler 1.16.0.pre.2
Using coffee-script-source 1.12.2
Using execjs 2.0.2
Using coffee-script 2.2.0
Using daemons 1.2.4
Fetching ffi 1.9.18
Installing ffi 1.9.18 with native extensions
Fetching ethon 0.10.1
Installing ethon 0.10.1
Using eventmachine 1.2.5
Using hike 1.2.3
Using json 2.1.0
Using multi_json 1.12.2
Using rack 1.5.5
Using rack-protection 1.5.3
Using rack-test 0.7.0
Fetching typhoeus 1.3.0
Installing typhoeus 1.3.0
Using ruby_dlrnapi 1.0.0 from https://github.com/halcyondude/ruby_dlrnapi.git (at master@ab830dc)
Using thread_safe 0.3.6
Using tzinfo 1.2.3
Using rufus-scheduler 2.0.24
Using sass 3.2.19
Using tilt 1.4.1
Using sinatra 1.4.8
Using sinatra-contrib 1.4.7
Using sprockets 2.10.2
Using thin 1.6.4
Using thor 0.20.0
Using smashing 1.0.0
Using twitter 6.1.0
Bundle complete! 2 Gemfile dependencies, 28 gems now installed.
Use `bundle info [gemname]` to see where a bundled gem is installed.
```

The ruby_dlrnapi gem is installed directly from git/source:

```
[you@yourbox dlrnapi-dashboard] $ bundle info ruby_dlrnapi
The latest bundler is 1.16.0.pre.3, but you are currently running 1.16.0.pre.2.
To install the latest version, run `gem install bundler --pre`
  * ruby_dlrnapi (1.0.0 ab830dc)
	Summary: A ruby client wrapper for https://github.com/softwarefactory-project/DLRN/blob/master/doc/api_definition.yaml
	Homepage: https://github.com/halcyondude/ruby_dlrnapi
	Path: /home/matyoung/.gem/ruby/2.4.0/bundler/gems/ruby_dlrnapi-ab830dca113b
```

Now start your dashboard!

```
smashing start
```

