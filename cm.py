# Import 3rd party libraries
import yaml


class ConfigurationManager:

    def __init__(self, configPath):
        self.configPath = configPath
        self.config = self.read_yaml_config()

    def read_yaml_config(self):
        """
        Reads a YAML configuration file and returns the contents as a Python dictionary.

        Parameters:
        - file_path: The path to the YAML file to be read.

        Returns:
        A dictionary containing the configuration parameters.
        """
        try:
            with open(self.configPath, "r") as file:
                config = yaml.safe_load(file)
            return config
        except FileNotFoundError:
            print(f"Error: The file '{self.configPath}' was not found.")
            return None
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML file: {exc}")
            return None

    def buildYoutubeActionConfigs(self):
        youtubeActionConfigs = []
        actionConfigs = []
        outputfile = self.config["outputfile"]
        for source in self.config["sources"]:
            if source["pipeline"] == "Youtube":
                actionConfigs = [
                    {
                        "url": source["url"],
                        "sheet": source["sheet"],
                        "timeindex": timeindex,
                        "outputfile": outputfile,
                    }
                    for timeindex in source["timeindexes"]
                ]
            youtubeActionConfigs = youtubeActionConfigs + actionConfigs
        return youtubeActionConfigs

    def buildArticleTablesConfigs(self):
        configs = []
        outputfile = self.config["outputfile"]
        for source in self.config["sources"]:
            if source["pipeline"] == "ArticleTables":
                source["outputfile"] = outputfile
                configs = configs + [source]

        return configs

    def buildArticleImagesConfigs(self):
        configs = []
        outputfile = self.config["outputfile"]
        for source in self.config["sources"]:
            if source["pipeline"] == "ArticleImages":
                source["outputfile"] = outputfile
                configs = configs + [source]

        return configs
