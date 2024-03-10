import nlpaug.augmenter.word as naw

# Example sentence to augment
text = "This is a sample sentence for data augmentation."

# Perform synonym replacement augmentation
aug = naw.SynonymAug(aug_src='wordnet')
augmented_text = aug.augment(text)