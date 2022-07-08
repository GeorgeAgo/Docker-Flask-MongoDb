# ΠΛΗΡΟΦΟΡΙΑΚΑ ΣΥΣΤΗΜΑΤΑ 2021-2022 
# Υποχρεωτική Εργασία
# Γιώργος Αγορίτσας Ε19002

Για την εκτέλεση του προγράμματος είναι κρίσιμο να έχει καταννοηθεί το περιεχόμενο που εξετάστηκε στο εργαστήριο του μαθήματος , συγκεκριμένα πως να χειριζόμαστε το Docker , το Flask και την MongoDb , όλα αυτά βασισμένα σε ένα GNU/Linux περιβάλλον. <br />
Ξεκινώντας πραγματοποιούμε την εξής εντολή :
```bash
sudo apt install docker docker-compose 
```
Το πρόγραμμα εκτελείται στη πόρτα 5000 μέσω flask ενώ η Mongodb στην πόρτα localhost . 
Όπως τονίζεται και στις οδηγίες της εργασίας έχω δημιουργήσει μία database "DigitalNotes" που στην αρχή είναι άδεια .
Για την δημιουργία του container εκτελώ την παρακάτω εντολή:
```bash
docker-compose up -d  
```
![](E19002/screenshots/arxiko.png )

Παρακάτω θα αναλυθούν οι λειτουργίες του προγράμματος καθώς και τα βήματα υλοποίησης του από τον χρήστη . <br />

Πρώτα από όλα υπογραμμίζουμε ότι κατά την εκχώρηση των στοιχείων από τον χρήστη στο πεδίο του url , το κάθε πεδίο χωρίζεται από το επόμενο με & και εχωρεί την τιμή αμέσως μετά το = .  <br />

Σε κάθε σφάλμα ή επιτυχημένο βήμα το πρόγραμμα επιστρέφει μηνύματα που εξηγούν αν οι διαδικασία πραγματοποιήθηκε επιτυχώς ή αν υπήρξε κάποιο σφάλμα , εξηγώντας τι πήγε λάθος . <br />

Σε κάθε παράλειψη συμπλήρωσης πεδίου , το πεδίο συμπληρώνεται με το None . <br />

## -> Λειτουργία Sign up 
![](E19002/screenshots/signup.png )
Δίνοντας :
```bash
http://localhost:5000/signup/?mail=a&username=a&name=a&password=a&role=0
```
Μπορούμε να δημιουργήσουμε έναν χρήστη στο σύστημα , ο οποίος θα έχει mail a , username a , name a , password a και role 1 άρα πρόκειται για admin , αντίστοιχα αν ήταν admin θα μπορούσε να βάλει role=1 . <br />
To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή και μόνο τότε ολοκληρώνεται η εγγραφή του χρήστη , και κατά την ολοκλήρωση της διαδικασίας αναγράφονται τα στοιχεία που τελικά εισάχθηκαν . <br />
Αν το username ή οποιοδήποτε άλλο πεδίο χρησιμοποιείται ήδη από άλλο χρήστη , τότε δεν γίνεται sign up και αναγράφεται το αντίστοιχο σφάλμα.

## -> Λειτουργία login
![](E19002/screenshots/login.png )
Δίνοντας :
```bash
http://localhost:5000/login/?mail=a&username=a&name=a&password=a
```
Πραγματοποιείται προσπάθεια σύνδεσης του αντίστοιχου χρήστη , αν τα στοιχεία είναι ορθά τότε πραγματοποιείται σύνδεση , επιστρέφοντας ένα μήνυμα ενημερώνοντας το χρήστη . <br />
Αν κάποιο από τα στοιχεία που εισάχθηκαν δεν υπάρχει στα δεδομένα μας , τότε το Login δεν πραγματοποιείται . <br />

## -> Λειτουργία createNote
![](E19002/screenshots/createnote.png )
Δίνοντας :
```bash
http://localhost:5000/CreateNote/?title=note1&text=text_tou_note1&tags=tag_tou_note1
```
Ο χρήστης που έχει πραγματοποιήσει login , εισάγει το τίτλο του note , το περιεχόμενό του (text χωρίς κενά) αλλά και τα tags του . 
Αν τα στοιχεία που εισήγαγε ο χρήστης είναι μοναδικά , τότε δημιουργείται το αντίστοιχο note αποθηκεύντας και την ημερομηνία δημιουργίας του.
Όμως αν έχει δημιουργηθεί ήδη τότε η λειτουργία ματαιώνεται ενημερώνοντας το χρήστη για το πρόβλημα . </br>

## -> Λειτουργία titleSearch
![](E19002/screenshots/titlesearch.png )
Δίνοντας :
```bash
http://localhost:5000/title_Search/?title=note1
```
Ο χρήστης δίνει στο πρόγραμμα το όνομα του note που ψάχνει και εκείνο εφόσον υπάρχει του επιστρέφει το τίτλο , τα tags αλλά και το text του . </br>
Αν δεν υπάρχει κάποιο note με το αντίστοιχο όνομα επιστρέφεται στο χρήστη το αντίστοιχο σφάλμα . </br>

## -> Λειτουργία tag_Search
![](E19002/screenshots/tagsearch.png )
Δίνοντας :
```bash
http://localhost:5000/tag_Search/?tags=tag_tou_note1
```
Ο χρήστης δίνει στο πρόγραμμα τη λέξη κλειδί (tag) του note που ψάχνει και εκείνο εφόσον υπάρχει του επιστρέφει το τίτλο , τα tags αλλά και το text του . Οι σημειώσεις που έχουν αυτό το tag εμφανίζονται με βάση την ημερομηνία δημιουργίας τους . </br>
Αν δεν υπάρχει κάποιο note με το αντίστοιχο tag επιστρέφεται στο χρήστη το αντίστοιχο σφάλμα . </br>

## -> Λειτουργία update
![](E19002/screenshots/update.png )
Δίνοντας :
```bash
http://localhost:5000/update/?title=note1
```
Ο χρήστης εισάγει στο πρόγραμμα το τίτλο του note που επιθυμεί να τροποποιήσει και εφόσον υπάρχει η αντίστοιχη σημείωση του δίνεται η δυνατότητα να αλλάξει τα πεδία : title , text , tags , με τον ίδιο τρόπο που ακολούθησε και κατά τη λειτουργία του createNote . </br>
Από την άλλη αν δεν βρεθεί ο τίτλος της σημείωσης επιστρέφεται στο χρήστη το αντίστοιχο σφάλμα . </br>

## -> Λειτουργία deleteNote
![](E19002/screenshots/deletenote.png )
Δίνοντας :
```bash
http://localhost:5000/deleteNote/?title=note1
```
Ο χρήστης δίνει στο πρόγραμμα το τίτλο του note που επιθυμεί να διαγράψει , αν βρεθεί το αντίστοιχο note , τότε διαγράφεται από τα δεδομένα μας . </br>
Από την άλλη αν δεν βρεθεί ο τίτλος της σημείωσης επιστρέφεται στο χρήστη το αντίστοιχο σφάλμα . </br>

## -> Λειτουργία sort
![](E19002/screenshots/sort.png )
Δίνοντας :
```bash
http://localhost:5000/sort/?sort=+
```
Ο χρήστης το μόνο που έχει να εισάγει είναι ο χρόνος που θα γίνει η χρονολογική σειρά , δηλαδή με + αν θέλει να γίνει ascending ή - για descending , με άλλα λόγια αν θέλει να εμφανιστούν πρώτα οι παλαιότερες ή πρώτα οι νεότερες σημειώσεις . </br>

## -> Λειτουργία delete
![](E19002/screenshots/deleteuser.png )
Δίνοντας :
```bash
http://localhost:5000/delete/?
```
Ο χρήστης αφού εισάγει την εντολή delete δεν χρειάζεται να προσθέσει τίποτα παραπάνω αφού με το που πατήσει enter , διαγράφεται ο λογαριασμός του , έμμεσα έτσι χάνει πρόσβαση στις λειτουργίες που είχε με το πρόγραμμα αυτό αλλά διαγράφονται οι σημειώσεις που είχε δημιουργήσει προηγουμένως . </br>

## Σε αυτό το σημείο περνάμε στις λειτουργίες που μπορεί να εκτελέσει μόνο ένας διαχειριστής , δηλαδή έχει πραγματοποιήσει sing up με role=1 . </br>

## -> Λειτουργία Insert_Admin
![](E19002/screenshots/insertAdmin.png )
Δίνοντας :
```bash
http://localhost:5000/Insert_Admin/?mail=b&username=b&name=b&password=b&role=1
```
Όταν κάποιος admin επιθυμεί να εισάγει κάποιον άλλο καινούεγιο διαχειριστή στο πρόγραμμα , εισάγει την εντολή Insert_Admin και στη συνέχεια συμπληρώνει τα πεδία mail , username , name , password , role=1 , με τα στοιχεία του νέου διαχειριστή . Με τη σειρά του ο καινούργιος διαχειριστής όταν προσπαθήσει να κάνει login απευθείας θα του ζητηθεί να αλλάξει κωδικό πρόσβασης για λόγους ασφαλείας .  </br>
Το μόνο πρόβλημα που μπορεί να προκύψει είναι να υπάρχει ήδη αυτός ο διαειρστής εγγεγραμένος στο πρόγραμμα , σε αυτή τη περίπτωση ενημερώνεται ο χρήστης για το σφάλμα και η εγγραφή του admin ματαιώνεται . </br>

## -> Λειτουργία delete_Admin
![](E19002/screenshots/deleteadmin.png )
Δίνοντας :
```bash
http://localhost:5000/delete_Admin/?username=a
```
Όταν κάποιος admin επιθυμεί να διαγράψει κάποιον χρήστη από τη βάση δεδομένων του προγράμματος , το μόνο που πρέπει να εισάγει είναι το αντίστοιχο username αυτού του χρήστη . Αν βρεθέι αυτός ο χρήστης στη βάση δεδομένων τότε διαγράφεται  . </br>
Αν όμως δεν είναι εγγεγραμμένος με το συγκεκριμένο username , τότε ενημερώνεται ο admin για το αντίστοιχο σφάλμα και η διαδικασία ματαιώνεται . </br>


# Βιβλιογραφία
Βοηθητικό υλικό για την εκπόνηση της εργασίας : </br>
-> Διαφάνειες του εργαστηρίου .</br>
-> Παρόμοια project στο Github .</br>
-> www.stackoverflow.com .</br>
-> www.geeksforgeeks.com .</br>

# ΓΙΩΡΓΟΣ ΑΓΟΡΙΤΣΑΣ Ε19002 8/7/2022
