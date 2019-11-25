#Brief configuration file for creating categories in the models
print("Loading Categories...")

tt_boosted_1J_category = 'tt_boosted_onejet'
tt_boosted_GE2J_category = 'tt_boosted_multijet'
tt_vbf_high_category = 'tt_vbf_highHpT'
tt_vbf_low_category = 'tt_vbf_highHpT'
tt_0jet_category = 'tt_0jet'

mt_boosted_1J_category = 'mt_boosted_1J'
mt_boosted_GE2J_category = 'mt_boosted_GE2J'
mt_vbf_low_category = 'mt_vbf_PTH_0_200'
mt_vbf_high_category = 'mt_vbf_PTH_GE_200'
mt_0jet_low_category = 'mt_0jet_PTH_0_10'
mt_0jet_high_category = 'mt_0jet_PTH_GE10'

et_0jet_low_category = 'et_0jetlow'
et_0jet_high_category = 'et_0jethigh'
et_boosted_1J_category = 'et_boosted1'
et_boosted_GE2J_category = 'et_boosted2'
et_vbf_low_category = 'et_vbflow'
et_vbf_high_category = 'et_vbfhigh'

em_0jet_low_category = 'em_0jetlow'
em_0jet_high_category = 'em_0jethigh'
em_boosted_1J_category = 'em_boosted1'
em_boosted_GE2J_category = 'em_boosted2'
em_vbf_low_category = 'em_vbflow'
em_vbf_high_category = 'em_vbfhigh'

tt_boosted_categories = []
tt_boosted_categories.append(tt_boosted_1J_category)
tt_boosted_categories.append(tt_boosted_GE2J_category)
tt_vbf_categories = []
tt_vbf_categories.append(tt_vbf_high_category)
tt_vbf_categories.append(tt_vbf_low_category)
tt_0jet_categories = []
tt_0jet_categories.append(tt_0jet_category)

tt_Categories = []
tt_Categories = tt_boosted_categories + tt_vbf_categories + tt_0jet_categories

mt_boosted_categories = []
mt_boosted_categories.append(mt_boosted_1J_category)
mt_boosted_categories.append(mt_boosted_GE2J_category)
mt_vbf_categories = []
mt_vbf_categories.append(mt_vbf_low_category)
mt_vbf_categories.append(mt_vbf_high_category)
mt_0jet_categories = []
mt_0jet_categories.append(mt_0jet_low_category)
mt_0jet_categories.append(mt_0jet_high_category)

mt_Categories = []
mt_Categories = mt_boosted_categories + mt_vbf_categories + mt_0jet_categories

et_boosted_categories = []
et_boosted_categories.append(et_boosted_1J_category)
et_boosted_categories.append(et_boosted_GE2J_category)
et_vbf_categories = []
et_vbf_categories.append(et_vbf_low_category)
et_vbf_categories.append(et_vbf_high_category)
et_0jet_categories = []
et_0jet_categories.append(et_0jet_low_category)
et_0jet_categories.append(et_0jet_high_category)

et_Categories = []
et_Categories = et_boosted_categories + et_vbf_categories + et_0jet_categories

em_boosted_categories = []
em_boosted_categories.append(em_boosted_1J_category)
em_boosted_categories.append(em_boosted_GE2J_category)
em_vbf_categories = []
em_vbf_categories.append(em_vbf_low_category)
em_vbf_categories.append(em_vbf_high_category)
em_0jet_categories = []
em_0jet_categories.append(em_0jet_low_category)
em_0jet_categories.append(em_0jet_high_category)

em_Categories = []
em_Categories = em_boosted_categories + em_vbf_categories + em_0jet_categories

tt_Categories = {'cat0':'cat0',
                 'cat1':'cat1',
                 'cat2':'cat2',
                 'cat3':'cat3',
                 'cat4':'cat4'}
mt_Categories = {'mt_0jet_PTH_0_10':'mt_0jet_PTH_0_10',
                 'mt_0jet_PTH_GE10':'mt_0jet_PTH_GE10',
                 'mt_vbf_PTH_0_200':'mt_vbf_PTH_0_200',
                 'mt_vbf_PTH_GE_200':'mt-vbf_PTH_GE_200',# typo fixy do
                 'mt_boosted_1J':'mt_boosted_1J',
                 'mt_boosted_GE2J':'mt_boosted_GE2J'}
et_Categories = {'et_0jet_PTH_0_10':'et_0jetlow',
                 'et_0jet_PTH_GE10':'et_0jethigh',
                 'et_vbf_PTH_0_200':'et_vbflow',
                 'et_vbf_PTH_GE_200':'et_vbfhigh',
                 'et_boosted_1J':'et_boosted1',
                 'et_boosted_GE2J':'et_boosted2'}
em_Categories = {'em_0jet_PTH_0_10':'em_0jetlow',
                 'em_0jet_PTH_GE10':'em_0jethigh',
                 'em_vbf_PTH_0_200':'em_vbflow',
                 'em_vbf_PTH_GE_200':'em_vbfhigh',
                 'em_boosted_1J':'em_boosted1',
                 'em_boosted_GE2J':'em_boosted2'}
Categories = {'tt':tt_Categories,
              'mt':mt_Categories,
              'et':et_Categories,
              'em':em_Categories}
