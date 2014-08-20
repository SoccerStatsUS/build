mkdir openfootball
cd openfootball/
git clone https://github.com/sportkit/sport.db.starter.ruby.git
sudo apt-get install bundler sqlite3 libsqlite3-dev emacs git-core
cd sport.db.starter.ruby/
sudo gem install sqlite3 -v '1.3.9'
bundle install
ruby server.rb
