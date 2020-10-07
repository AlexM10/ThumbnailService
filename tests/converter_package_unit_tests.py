import unittest
from src.Controller.Converter.converter import ToThumbNailConverter
from PIL import Image
from tests.size_holder import SizeHolder
from src.Controller.Converter.dimension_holder import DimensionHolder
from src.Controller.Converter.converter_interface import IConverter
from src.Controller.Converter.image_dimension_calculator_interface import ImageDimensionCalculatorInterface
from src.Controller.Converter.image_dimension_calculator import ThumbnailDimensionCalculator


class MyUnitTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls._image_to_resize = Image.open("sample.jpg")
        cls._org_width = cls._image_to_resize.size[0]
        cls._org_height = cls._image_to_resize.size[1]

    @classmethod
    def tearDownClass(cls) -> None:
        cls._image_to_resize.close()


class DimensionHolderTests(MyUnitTest):

    def setUp(self):
        self.target_width = 200
        self.target_height = 200
        self.dimensions = DimensionHolder(img=self._image_to_resize, width=self.target_width
                                          , height=self.target_height)

    def test_get_org_width(self):
        self.assertEqual(self._org_width, self.dimensions.get_org_width())

    def test_get_org_height(self):
        self.assertEqual(self._org_height, self.dimensions.get_org_height())

    def test_get_target_width(self):
        self.assertEqual(self.target_width, self.dimensions.get_target_width())

    def test_get_target_height(self):
        self.assertEqual(self.target_width, self.dimensions.get_target_height())


class ThumbnailDimensionCalculatorTest(MyUnitTest):

    def setUp(self) -> None:
        self._dimensions = DimensionHolder(img=self._image_to_resize, width=200, height=200)
        self.calculator = ThumbnailDimensionCalculator()

    def test_is_calculator_implements_image_dimension_calculator_interface(self):
        ans = issubclass(self.calculator, ImageDimensionCalculatorInterface)
        self.assertEqual(ans, True)

    def test_calculate_ratio(self):
        self.assertEqual(self.calculator._ThumbnailDimensionCalculator__calculate_ratio(self._dimensions), 0.8,
                         msg="Thumbnail dimension calculator test calculator ratio wrong ratio")

    def test_calculate_new_dimensions(self):
        test_new_width, test_new_height = self.calculator.calculate_new_dimensions(self._dimensions)
        self.assertAlmostEqual(200, test_new_width, msg="Thumbnail dimension calculator test calculate new "
                                                        "dimensions wrong width", delta=1)
        self.assertAlmostEqual(134, test_new_height, msg="Thumbnail dimension calculator test calculate new "
                                                         "dimensions wrong height", delta=1)


class ThumbNailConverterTest(MyUnitTest):

    def setUp(self):
        self._size_org = SizeHolder(width=self._org_width, height=self._org_height)
        self._original_ratio = self._size_org.calc_ratio()
        self.converter = ToThumbNailConverter()

    """Validates that the Converter implements the IConverter interface"""

    def test_is_converter_implements_IConverter(self):
        ans = issubclass(self.converter, IConverter)
        self.assertEqual(ans, True)

    """Tests for not_valid function"""

    def set_test_not_valid(self, test_width, test_height):
        dimensions = DimensionHolder(self._image_to_resize, test_width, test_height)
        ans = self.converter._ToThumbNailConverter__not_valid(dimensions)
        return ans

    """not_valid function test for true"""

    def test_not_valid_true(self):
        self.assertEqual(self.set_test_not_valid(251, 168), True, "test_not_valid_true got false expected true")

    """not_valid function test for false"""

    def test_not_valid_false(self):
        self.assertEqual(self.set_test_not_valid(250, 167), False, "test_not_valid_true got true expected false")

    """Test for create_thumbnail_with_borders checks if the box of the right size"""

    def test_create_thumbnail_with_borders(self):
        image_size = self._size_org.get_size()[0], self._size_org.get_size()[1]
        img = self.converter._ToThumbNailConverter__create_thumbnail_with_borders(
            (300, 300), image_size, self._image_to_resize)
        self.assertEqual(img.size[0], 300, "test_create_thumbnail_with_borders wrong box width")
        self.assertEqual(img.size[1], 300, "test_create_thumbnail_with_borders wrong box height")

    """Tests Ratios after resizing, tests tge resize_image function"""
    """Test Ratio For resizing image to 200, 134"""

    def set_test_ratio(self, test_width: int, test_height: int) -> SizeHolder:
        dimensions = DimensionHolder(self._image_to_resize, test_width, test_height)
        img = self.converter._ToThumbNailConverter__resize_image(self._image_to_resize, dimensions)
        return SizeHolder(img.size[0], img.size[1])

    def test_ratio_case1(self):
        new_size = self.set_test_ratio(200, 134)
        self.assertAlmostEqual(new_size.calc_ratio(), self._original_ratio,
                               msg="testCase1 ratio is false", delta=0.01)

    """Test Ratio For resizing image to 200, 200"""

    def test_ratio_case2(self):
        new_size = self.set_test_ratio(200, 200)
        self.assertAlmostEqual(new_size.calc_ratio(), self._original_ratio,
                               msg="testCase2 ratio is false", delta=0.01)

    """ Test Ratio For resizing image to 300, 134"""

    def test_ratio_case3(self):
        new_size = self.set_test_ratio(300, 134)
        self.assertAlmostEqual(new_size.calc_ratio(), self._original_ratio,
                               msg="testCase3 ratio is false", delta=0.01)

    """Test Ratio For resizing image to 300, 300"""

    def test_ratio_case4(self):
        new_size = self.set_test_ratio(300, 300)
        self.assertAlmostEqual(new_size.calc_ratio(), self._original_ratio,
                               msg="testCase4 ratio is false", delta=0.01)

    """Test Ratio For resizing image to 134, 300"""

    def test_ratio_case5(self):
        new_size = self.set_test_ratio(134, 300)
        self.assertAlmostEqual(new_size.calc_ratio(), self._original_ratio,
                               msg="testCase5 ratio is false", delta=0.01)

    """Test Ratio For resizing image to 134, 134"""

    def test_ratio_case6(self):
        new_size = self.set_test_ratio(134, 134)
        self.assertAlmostEqual(new_size.calc_ratio(), self._original_ratio,
                               msg="testCase6 ratio is false", delta=0.01)

    """Convert function Tests"""

    def set_test_convert(self, test_width, test_height):
        img = self.converter.convert(given_img=self._image_to_resize, target_width=test_width,
                                     target_height=test_height)
        return img.size[0], img.size[1]

    """Test for target width of 200 and target height of 134"""

    def test_convert_case1(self):
        img_width, img_height = self.set_test_convert(200, 134)
        self.assertAlmostEqual(img_width, 200, msg="test_convert_case1 wrong  width")
        self.assertAlmostEqual(img_height, 134, msg="test_convert_case1 wrong  height")

    """Test for target width of 200 and target height of 200"""

    def test_convert_case2(self):
        img_width, img_height = self.set_test_convert(200, 200)
        self.assertAlmostEqual(img_width, 200, msg="test_convert_case2 wrong  width")
        self.assertAlmostEqual(img_height, 200, msg="test_convert_case2 wrong  height")

    """Test for target width of 300 and target height of 134"""

    def test_convert_case3(self):
        img_width, img_height = self.set_test_convert(300, 134)
        self.assertAlmostEqual(img_width, 300, msg="test_convert_case3 wrong  width")
        self.assertAlmostEqual(img_height, 134, msg="test_convert_case3 wrong  height")

    """Test for target width of 300 and target height of 300"""

    def test_convert_case4(self):
        img_width, img_height = self.set_test_convert(300, 300)
        self.assertAlmostEqual(img_width, 300, msg="test_convert_case4 wrong  width")
        self.assertAlmostEqual(img_height, 300, msg="test_convert_case4 wrong  height")

    """Test for target width of 134 and target height of 300"""

    def test_convert_case5(self):
        img_width, img_height = self.set_test_convert(134, 300)
        self.assertAlmostEqual(img_width, 134, msg="test_convert_case5 wrong  width")
        self.assertAlmostEqual(img_height, 300, msg="test_convert_case5 wrong  height")

    """Test for target width of 134 and target height of 134"""

    def test_convert_case6(self):
        img_width, img_height = self.set_test_convert(134, 134)
        self.assertAlmostEqual(img_width, 134, msg="test_convert_case6 wrong  width")
        self.assertAlmostEqual(img_width, 134, msg="test_convert_case6 wrong  height")



