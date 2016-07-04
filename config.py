

MIN_LENGTH = 35

out_dir = '/home/vda/test/generated'
test_dir = '/media/vda/C95D42734B09AB7D/test'

model_file = 'model.pickle'

LABEL_LIST = ['horizontal', 'vertical', 'u', 'alpha', 'circle_left', 'hat', 'z', 'derivative', 'six', 'triangle', 'random', 'greater_than', 'square_root']
WHITE_LIST = [] # ['hat']
BLACK_LIST = ['six', 'circle_left', 'square_root']
LABELS = { value : index for index, value in enumerate(LABEL_LIST) }
