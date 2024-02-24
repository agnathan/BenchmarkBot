import os
import glob
from cm import ConfigurationManager

# Import the Benchmarkbot Pipeline class
from pipeline import Pipeline

# Import the Benchmarkbot Actions
from botActions.youtubeDownloadAction import YoutubeDownloadAction
from botActions.youtubeScreenShotAction import YoutubeScreenShotAction
from botActions.openvinoTextRecognitionAction import OpenVINOTextRecognitionAction
from botActions.ocrTextRecognitionAction import OCRTextRecognitionAction
from botActions.lemmatizationAction import LemmatizationAction
from botActions.namedEntityRecognitionAction import NamedEntityRecognitionAction
from botActions.ArticleTablesDownloadAction import ArticleTablesDownloadAction
from botActions.ArticleImageDownloadAction import ArticleImagesDownloadAction
from botActions.nlpAction import NLPAction
from botActions.excelWriteAction import ExcelWriteAction

# Print semi-annoying bot announcement title
print(
    """
██████╗ ███████╗███╗   ██╗ ██████╗██╗  ██╗███╗   ███╗ █████╗ ██████╗ ██╗  ██╗██████╗  ██████╗ ████████╗
██╔══██╗██╔════╝████╗  ██║██╔════╝██║  ██║████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝█████╗  ██╔██╗ ██║██║     ███████║██╔████╔██║███████║██████╔╝█████╔╝ ██████╔╝██║   ██║   ██║   
██╔══██╗██╔══╝  ██║╚██╗██║██║     ██╔══██║██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗ ██╔══██╗██║   ██║   ██║   
██████╔╝███████╗██║ ╚████║╚██████╗██║  ██║██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗██████╔╝╚██████╔╝   ██║   
╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝   
                                                                                                             
      """
)
# Read in the BenchmarkBot configuration file
cm = ConfigurationManager("bot.yaml")

# Define the Benchmarkbot AI Pipelines
youtubePipeline = Pipeline()
youtubePipeline.add_action(YoutubeDownloadAction())
youtubePipeline.add_action(YoutubeScreenShotAction())
youtubePipeline.add_action(OCRTextRecognitionAction())
youtubePipeline.add_action(NLPAction())
youtubePipeline.add_action(ExcelWriteAction())

# Pipeline for the Article Images
articleImageConfigs = cm.buildArticleImagesConfigs()
for config in articleImageConfigs:
    cacheDir = ArticleImagesDownloadAction().run(config)
    imgFiles = glob.glob(f"{cacheDir}\\*png")

    for imgfile in imgFiles:
        ocrfile = OCRTextRecognitionAction().run(config, imgfile)
        NLPAction().run(config, ocrfile)
    ExcelWriteAction().run(config, os.path.join(cacheDir, "nlp.json"))

# Process configs that use ArticleTables
atConfigs = cm.buildArticleTablesConfigs()
for config in atConfigs:
    cacheDir = ArticleTablesDownloadAction().run(config)
    tableFiles = glob.glob(f"{cacheDir}\\*ArticleTable.json")

    for tableFile in tableFiles:
        NLPAction().run(config, tableFile)

    ExcelWriteAction().run(config, cacheDir + "\\ArticleTable.json")


ytConfigs = cm.buildYoutubeActionConfigs()
# print(ytConfigs)
for config in ytConfigs:
    youtubePipeline.execute(config)
