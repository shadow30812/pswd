# Command-Line Password Manager

Hey there! Ever wish you had a super simple, super secure spot for all your passwords? Well, you've found it! This little tool runs right from your command line and uses some serious encryption to keep your passwords safe and sound on your own computer. The best part? Everything is unlocked with a single master password that only you know!

## What's Inside?

* **Super Strong Encryption:** It uses some top-notch encryption (called Fernet, if you're curious!) to lock up all your passwords.
* **Your Password is the *Only* Key:** The secret key that locks and unlocks everything? It's made on-the-fly from your master password. We never, ever save it to a file!
* **Awesome Password Generator:** Need a password that's tough to crack? We've got you covered! The generator script can whip one up in a second, and you can tell it exactly how you like it.
* **You're in Control:** All your info is saved locally in a `passwords.txt` file. It's your data, on your machine. Always.
* **Easy to Use:** Just type a few simple commands to view or add your passwords. Easy peasy!

## 🔐 How it Keeps Your Stuff Safe

So, how does it all stay safe? Simple! The whole system is built so that we know absolutely nothing about your passwords. Here's the lowdown:

1. **Setting up is a snap:** The very first time you run it, you'll get to create your one-and-only master password.
2. **We add a 'salt':** The app makes a unique little file called `salt.bin`. Think of it like a secret ingredient that makes your encryption key totally unique to you.
3. **Creating the magic key:** Every time you log in, the app mixes your master password and that salt together to create the secret key.
4. **And... poof! It's gone:** The best part? This key only exists in your computer's memory while the app is running. The moment you close it, the key vanishes into thin air.
5. **The key fits!** The app knows you typed the right password because it's the only one that can successfully unlock your stuff. If it works, you're in!

> **Heads up!** Since we never save your master password, if you forget it, there's absolutely **no way** to get your data back. Your encrypted passwords will be locked away for good. So please, please pick something you'll remember!

## What You'll Need

Alright, what do you need to get started? It's not much! First, make sure you have Python 3 on your computer. Then, you just need to install one library. Open up your terminal and type:

```bash
pip install cryptography
```

## How to Use It

Ready to jump in? Getting started is a breeze! There are two main scripts you'll use.

### 1. The Password Manager (`password_manager.py`)

This is your command center for your password vault.

#### Setting Up

Just run the script in your terminal. The first time, it'll walk you through creating your master password.

```bash
python password_manager.py
```

#### Day-to-Day Use

After you're set up, just run the same command and pop in your master password when it asks.

```bash
python password_manager.py
```

You'll get a simple menu:

* **[V]iew:** Shows you all your saved passwords.
* **[A]dd:** Lets you add a new password to your vault.
* **[Q]uit:** Closes the program.

### 2. The Password Generator (`password_generator.py`)

This little helper is perfect for when you need to create a brand new, super-strong password.

#### Basic Use

You just have to tell it how long you want the password to be.

```bash
# This makes a 16-character password with everything included
python password_generator.py 16
```

#### Fun Options

Want to mix it up? You can tell it to leave out numbers or special characters.

```bash
# Makes a 20-character password without any numbers
python password_generator.py 20 --no-numbers

# Makes a 12-character password without any special characters
python password_generator.py 12 --no-specials

# Makes a 24-character password with only letters
python password_generator.py 24 --no-numbers --no-specials
```

After it makes a password, it'll ask if you want to save it. If you say yes, it'll just ask for your master password to lock it up safely in your vault.

## What Files Does It Make?

So, what files will you see pop up? Just a couple:

* `passwords.txt`: This is where all your encrypted info lives. And don't worry, it just looks like a bunch of random nonsense to anyone who doesn't have your master password!
* `salt.bin`: This is that special 'salt' file we talked about. It's not a secret, but it's super important for making your key, so definitely **don't delete it!**

And hey, we've already added these to the `.gitignore` file for you, so you won't accidentally send them to a public place like GitHub. We've got your back!

*Disclaimer: This password manager/generator should not be used to store sensitive information or important passwords. The developer does not guarantee the safety of stored passwords, this is mostly a fun project good for storing non-sensitive passwords for common login portals.*
