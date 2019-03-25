
import numpy as np

class numpy_util():
	 
	def get_avg_from_two_vectors(self,first_vec,second_vec):
		sum = np.add(first_vec,second_vec)
		avg = np.divide(sum, 2)

		return avg
	
	def get_cosine_similarity(self,first_vec, second_vec):
		cosine_similarity = np.dot(first_vec, second_vec)/\
                                    (np.linalg.norm(first_vec) * np.linalg.norm(second_vec))
		return cosine_similarity


	def subtract_two_vectors(self,first,second):
		result = np.subtract(first,second)
		return result
	
	def add_two_vectors(self,first,second):
		result = np.add(first,second)
		return result
