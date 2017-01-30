import unittest

import sfsf_config_test
import epub_to_txt_parser_test
import txt_pre_processor_test
import training_data_factory_test
import deep_learning_model_test

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest( unittest.makeSuite( sfsf_config_test.SFSFConfigTest ) )
    test_suite.addTest( unittest.makeSuite( epub_to_txt_parser_test.EpubToTxtParserTest ) )
    test_suite.addTest( unittest.makeSuite( txt_pre_processor_test.TxtPreProcessorTest ) )
    test_suite.addTest( unittest.makeSuite( training_data_factory_test.TrainingDataFactoryTest ) )
    test_suite.addTest( unittest.makeSuite( deep_learning_model_test.DeepLearningModelTest ) )

    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run( test_suite )
