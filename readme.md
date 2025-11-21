!!!Progetto

Progetto universitario "Ghost 'N Goblins".

A cura di:
Riccardo La Rocca: Matricola n. 388955 
Diego Illari: Matricola n. 391931

Ricreata a scopo didattico una porzione del gioco: Ghosts 'n Goblins (1985) in linguaggio Python utilizzando la libreria grafica G2D (Pygame, Tkinter).


!!!Regole di gioco
Il gioco permette di muoversi nelle quattro direzioni utilizzando i tasti: ←↑→↓
E' inoltre possibile colpire ed eliminare gli Zombie tramite le torce: spacebar

Eliminazione dei personaggi:
Arthur (il protagonista) può essere eliminato cadendo nelle buche (disegnate sullo sfondo) o tramite la collisione con gli Zombie.
Gli zombie, oltre a cadere nelle buche, possono essere colpiti dalle torce lanciate da Arthur venendo eliminati definitivamente.


!!!Testing
Per eseuire i test sulle classi è necessario utilizzare nella shell il comando: python -m unittest *test_file_name*.py
Ad esempio, per testare il comportamento di arthur bisognerà digitare il comando: python -m unittest test_arthur.py
comandi:
python -m unittest test_arthur.py
python -m unittest test_zombie.py
python -m unittest test_flame.py
python -m unittest test_torch.py
python -m unittest test_platform_and_gravestone.py