// Connect to the 'elevatus' database
db = db.getSiblingDB('elevatus');

// Create a user with dbOwner role for the 'elevatus' database
db.createUser({
  user: 'elevatus',
  pwd: 'elevatus',
  roles: [
    {
      role: 'dbOwner',
      db: 'elevatus',
    },
  ],
});

// Create collections 'users' and 'candidates'
db.createCollection('users');
db.createCollection('candidates');
