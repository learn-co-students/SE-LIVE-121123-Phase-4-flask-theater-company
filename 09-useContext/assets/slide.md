---
theme : "night"
transition: "slide"
highlightTheme: "monokai"
slideNumber: false
title: "P4L6 - REST API Authorization with Flask"
verticalSeparator: 'xxx'
presentation:
    width: 1500
    height: 1000

---

## Authorization with Flask

![flask-1](./flask-1.png)

---

## Learning Objectives
* Understand the dangers of plaintext passwords {.fragment .fade-up}
* Understand the concept of hashing {.fragment .fade-up}
* Differentiate between hashing and encryption {.fragment .fade-up}
* Know about rainbow tables {.fragment .fade-up}
* Understand the concept of salting {.fragment .fade-up}
* Be able to use the `bcrypt` library to hash passwords {.fragment .fade-up}

---

### 🚫 Storing Passwords as Plaintext is BAD 🚫

![godaddy-breach](./godaddy-breach.png)

---

### Some breaches are bigger than others

![dailyquiz-breach](./dailyquiz-breach.png) 

![monster-breach](./monster-breach.png) {.fragment .fade-up}

---

### Even the big companies get it wrong

![facebook-breach](./facebook-breach.png)

---

### Hackers are paying attention

![rockyou2021](./rockyou2021.png)

---

### Protecting Passwords with Hashing

![Hash-Algorithm](./Hash-Algorithm.png)

---

### Hashing vs Encryption

![Hashing-definition](./Hashing-definition.jpg)

---

### Hashing alone is not enough

![rainbow-1](./rainbow-1.jpg)

---

### Salting

![salting-and-hashing](./Hash-plus-Salt-1-1024x516.webp)

---

### Salting with `bcrypt`
 
![bcrypt](./bcrypt.png)

#### Let's dive into the code! 🤿 {.fragment .fade-up}


