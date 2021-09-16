class Pila:
	"""Representa una pila con los metodos apilar, desapilar, 
	verificar si está vacia.
	"""
	
	def __init__(self):
		"""Crea una pila vacia."""

		self.items = []
		self.largo = 0

	def __len__(self):
		return self.largo

	def esta_vacia(self):
		"""Devuelve True si la lista esta vacia, de lo contrario False."""
		
		return len(self.items) == 0

	def apilar(self, x):
		"""Apila un elemento 'x'."""
		
		self.items.append(x)
		self.largo += 1

	def desapilar(self):
		"""Devuelve el elemento tope y lo elimina de la pila.
		Si la pila está vacia, levanta una excepción.
		"""
		if self.esta_vacia():
			raise IndexError('La pila está vacía.')

		self.largo -= 1
		return self.items.pop()

	def ver_tope(self):
		"""Devuelve el ultimo elemento que se agrego a la pila."""
		
		if len(self.items) == 0: return None
		
		return self.items[len(self.items)-1]
	
	def obtener_pila(self):
		return self.items
		