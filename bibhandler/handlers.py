from __future__ import print_function
from __future__ import division
from . import C_

import bibtexparser

###################################################################################################################################################

class Ref():
	def __init__(self, name, entry_type, info_dict,
		invalid_attrs=None,
		uses_arxiv_format=True,
		):
		self.name = name
		self.entry_type = entry_type
		self.info_dict = info_dict.copy()
		self.attrs = self.info_dict.keys() if invalid_attrs is None else [k for k in self.info_dict.keys() if not k in invalid_attrs]
		self.uses_arxiv_format = uses_arxiv_format
		self.arxiv_id = self.info_dict.get('arxivid', None) if self.uses_arxiv_format else None
		if not self.arxiv_id is None and 'journal' in info_dict.keys():
			self.info_dict.pop('journal')
		#print(self.arxiv_id)

	def __repr__(self):
		txt = '@'+self.entry_type+'{'+self.name+',\n'
		for attr in self.attrs:
			v = self.info_dict.get(attr, None)
			if v is None:
				continue
			v = v.replace('{', '').replace('}', '')
			txt += attr+' = {'+v+'},\n'

		if not self.arxiv_id is None:
			txt += 'journal = {'+f'arXiv preprint arXiv:{self.arxiv_id}'+'},\n'

		txt += '}'
		return txt

class RefsHandler():
	def __init__(self, filedir,
		invalid_attrs=None,
		):
		self.filedir = filedir
		self.refs = []
		with open(self.filedir) as bibtex_file:
			ref_dict = bibtexparser.load(bibtex_file).entries_dict
			ref_names = ref_dict.keys()
			for ref_name in ref_names:
				id = ref_dict[ref_name].pop('ID')
				entry_type = ref_dict[ref_name].pop('ENTRYTYPE')
				d = ref_dict[ref_name]
				#print(d)
				self.refs.append(Ref(id, entry_type, d, invalid_attrs))

	def __repr__(self):
		txt = ''
		for ref in self.refs:
			txt += str(ref)+'\n'
		return txt

	def export(self, save_rootdir):
		save_filedir = save_rootdir+'/'+self.filedir.split('/')[-1]
		#print(save_filedir)
		print(self, file=open(save_filedir, 'w'))