class color:
	'''
	Pouze pro vypis v barvach'''

	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'


class Cell:
	'''
	Reprezentuje datovou strukturu pro matici pro BPO'''

	def __init__(self):
		self.stav = None
		self.cena = None
		self.omezeni_na_stav = [0, 0.5, 1, 1.5]
		self.omezeni_akcni_vel = [-1, -0.5, 0, 0.5, 1]
		self.optimalni_u = None
		self.budouci_stav = None
		self.iterace = None


# Belmanuv princip
def main() -> None:
	print(color.BOLD + color.PURPLE + 'Belmanuv princip optimality program' + color.END)
	print(
		color.BOLD
		+ color.CYAN
		+ 'Vystup je ve forme textu od nulte do posledni N iterace kde je vzdy vypsan nejoptimalnejsi akcni zasah a na jaky stav to vede'
		+ color.END
	)

	# Definice poctu radku
	pocet_radku = 4  # Odpovida poctu omezeni na stavy
	pocet_sloupecku = 2  # Odpovida poctu kroku
	matice_bpo = []

	# Vytvoreni matice, kde kazda polozka je trida Cell. Matice má rozměry pocet_radku x pocet_sloupecku
	matice_bpo = [[Cell() for _ in range(pocet_radku)] for _ in range(pocet_sloupecku + 1)]

	# prvni cela iterace bude jen pro nastaveni vsech stavu a cisla iterace pro pozdejsi pouziti
	iterace = -1
	for sloupec_matice in matice_bpo:
		# list_bunek reprezentuje sloupec matice
		# Pro kazdy radek je treba vedet jeho cislo
		i = 0
		iterace = iterace + 1
		for bunka in sloupec_matice:
			# Nastaveni stavu bunky
			bunka.stav = bunka.omezeni_na_stav[i]
			bunka.iterace = iterace
			i = i + 1

	# Dopocitani cost funkce pro konečný stav
	for i in range(pocet_radku):
		matice_bpo[pocet_sloupecku][i].cena = (
			matice_bpo[pocet_sloupecku][i].stav * matice_bpo[pocet_sloupecku][i].stav
		)

	# Samotne reseni BPO
	# Provadime iteraci od posledního sloupce - 1 (tedy předposledního)
	for i in range(pocet_sloupecku):
		# Chceme zacit od N-1 iterace, protoze posledni iterace ma uz spocitane cost funkce
		aktualni_sloupec = pocet_sloupecku - i - 1  # Odecitame i protoze chceme jit od konce
		for radek in range(pocet_radku):

			# Iterujeme pres vsechny mozne u, ktere se daji aplikovat
			for u in matice_bpo[0][0].omezeni_akcni_vel:
				# Pocitame podle rovnice systemu, v jakem budoucim stavu bychom se pomoci akcni veliciny mohli nachazet
				# Nyni se muze resit rovnice systemu a ta je x_k+1 = uk + xk
				x_k_plus_1 = u + matice_bpo[aktualni_sloupec][radek].stav

				# Dostanu x_k_plus_1 pak je treba zkontrolovat jestli je to stav ve kterem se muzu nachazet
				# Jestli nemuzu nepokracujeme dal a jdeme na dalsi akcni zasah
				if x_k_plus_1 not in matice_bpo[0][0].omezeni_na_stav:
					continue

				# Nyni je treba nalezt bunku, ktera v tom budoucim kroku je prave ta se stavem x_k_plus_1
				for kazdy_budouci_stav in range(pocet_radku):
					# Pokud nam vyjde výsledek ve kterem se x_k+1 nachazi v omezeni tak muzeme spocitat cost funkci
					if x_k_plus_1 != matice_bpo[aktualni_sloupec + 1][kazdy_budouci_stav].stav:
						continue
					# Vypocet cost funkce
					cost_funkce = 0.5 * (u * u) + matice_bpo[aktualni_sloupec + 1][kazdy_budouci_stav].cena

					# Nyni zbyva porovnat jestli cost_funkce je nejmensi, pokud ano tak ji ulozit do ceny pro danou bunku
					if (
						matice_bpo[aktualni_sloupec][radek].cena is None
						or matice_bpo[aktualni_sloupec][radek].cena > cost_funkce
					):
						matice_bpo[aktualni_sloupec][radek].cena = cost_funkce
						matice_bpo[aktualni_sloupec][radek].optimalni_u = u
						matice_bpo[aktualni_sloupec][radek].budouci_stav = x_k_plus_1
					# TODO: neni tady moznost v pripade ze by byly 2 optimalni cesty

	# Slouzi pouze na projeti vsech bunek v matici a jejich vypsani pro uzivatele
	for iterace in range(pocet_sloupecku):
		text = f'N =  {iterace}'
		print(color.BOLD + color.RED + text + color.END)
		for e in range(pocet_radku):
			print(
				f'Optimální u: {matice_bpo[iterace][e].optimalni_u} stavy: {matice_bpo[iterace][e].stav} -> {matice_bpo[iterace][e].budouci_stav} pro iteraci {matice_bpo[iterace][e].iterace} -> {matice_bpo[iterace][e].iterace +1}'
			)


if __name__ == '__main__':
	main()
