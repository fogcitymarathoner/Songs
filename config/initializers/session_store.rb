# Be sure to restart your server when you modify this file.

# Your secret key for verifying cookie session data integrity.
# If you change this key, all old sessions will become invalid!
# Make sure the secret is at least 30 characters and all random, 
# no regular words or you'll be exposed to dictionary attacks.
ActionController::Base.session = {
  :key         => '_songs_session',
  :secret      => '9a1b58c501f3ff8de03046b349f5ebbb1613659d99f8ede7c477f90649bea690d6ed17584347174628cb18ef39d1f15618d7daa8bf52623596ace9bb280932d1'
}

# Use the database for sessions instead of the cookie-based default,
# which shouldn't be used to store highly confidential information
# (create the session table with "rake db:sessions:create")
# ActionController::Base.session_store = :active_record_store
