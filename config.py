

MIN_LENGTH = 35

out_dir = '/home/vda/MouseGestureRecognition/generated'
test_dir = '/media/vda/C95D42734B09AB7D/test'

model_file = 'model.pickle'

LABEL_LIST = ['alpha', 'circle_left', 'derivative', 'gamma', 'greater_than',
				'hat', 'horizontal', 'less_than', 'N', 'random', 'six', 'square',
				'square_root', 'tilda',
				 'triangle', 'u', 'vertical', 'z']
WHITE_LIST = [] # ['hat']
BLACK_LIST = ['derivative']
LABELS = { value : index for index, value in enumerate(LABEL_LIST) }
