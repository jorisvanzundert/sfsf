from sfsf import sfsf_config
from sfsf import training_data_factory

# sfsf_config.set_env( sfsf_config.DEVELOPMENT )

# main
training_data_fact = training_data_factory.TrainingDataFactory()
training_result = training_data_fact.create_by_indices( 'wpg_data.csv', (1,52,-600,-549), source=sfsf_config.TXT )
