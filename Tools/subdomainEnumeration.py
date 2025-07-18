import re
from commands import Commands
from files import Files
from request import Requests
from general import General
from globalEnv import GlobalEnv


class SubdomainEnumeration:
    def __init__(self):
        self.__crtSHsiteUrl = f'https://crt.sh/json?q='

    def __CrtSh(self):
        response = Requests.Get(url=f"{self.__crtSHsiteUrl}{GlobalEnv.GetDomain()}")
        Files.SaveTextToFile(response.text, f"{GlobalEnv.GetCrtSH()}", 'w')
        Files.SaveTextToFile(response.text, f"{GlobalEnv.GetLogFile()}")
        if response.status_code == 200:
            domains = General.ExtractDomainsFromJsonFile(GlobalEnv.GetCrtSH())
            Files.WriteListToFile(GlobalEnv.GetSubDomainsPath(), 'a', domains)
            Files.WriteListToFile(GlobalEnv.GetCrtShText(), 'w', domains)

    def __Subfinder(self):
        commands = Commands.SubfinderCommands()
        for c in commands:
            General.ExecuteCommand(c, GlobalEnv.GetSubfinder(), True)

    def __Sublist3r(self):
        commands = Commands.Sublist3rCommands()
        for c in commands:
            General.ExecuteCommand(c, GlobalEnv.GetSublist3r(), True)

    def __Amass(self):
        commands = Commands.AmassCommands()
        for c in commands:
            General.ExecuteCommand(c, GlobalEnv.GetAmass())
        amassResult = General.ExtractDomainsFromTextFile(GlobalEnv.GetAmass())
        Files.WriteListToFile(GlobalEnv.GetSubDomainsPath(), 'a', amassResult)
        Files.WriteListToFile(GlobalEnv.GetLogFile(), 'a', amassResult)
        Files.RemoveDuplicateFromFile(GlobalEnv.GetSubDomainsPath())

    def __AssetFinder(self):
        commands = Commands.AssetFinderCommands()
        for c in commands:
            General.ExecuteCommand(c, GlobalEnv.GetAssetFinder(), True)

    def __Chaos(self):
        commands = Commands.ChaosCommands()
        for c in commands:
            General.ExecuteCommand(c, GlobalEnv.GetChaos(), True)

    def __Httpx(self):
        General.RemoveOutOfScopeFromSubdomains(GlobalEnv.GetSubDomainsPath())
        Files.RemoveDuplicateFromFile(GlobalEnv.GetSubDomainsPath())
        commands = Commands.HttpxCommands()
        i = 1
        for c in commands:
            if i == 1:
                General.ExecuteCommand(c, GlobalEnv.GetHttpx())
                Files.CopyFromTo(GlobalEnv.GetTempFile(), GlobalEnv.GetHttpx())
            elif i == 2:
                General.ExecuteCommand(c, GlobalEnv.GetHttpx2xx())
                Files.CopyFromTo(GlobalEnv.GetTempFile(), GlobalEnv.GetHttpx2xx())
                Files.RemoveDuplicateFromFile(GlobalEnv.GetHttpx2xx())
            elif i == 3:
                General.ExecuteCommand(c, GlobalEnv.GetHttpx3xx())
                Files.CopyFromTo(GlobalEnv.GetTempFile(), GlobalEnv.GetHttpx3xx())
                Files.RemoveDuplicateFromFile(GlobalEnv.GetHttpx3xx())
            elif i == 4:
                General.ExecuteCommand(c, GlobalEnv.GetHttpx4xx())
                Files.CopyFromTo(GlobalEnv.GetTempFile(), GlobalEnv.GetHttpx4xx())
                Files.RemoveDuplicateFromFile(GlobalEnv.GetHttpx4xx())
            elif i == 5:
                General.ExecuteCommand(c, GlobalEnv.GetHttpx5xx())
                Files.CopyFromTo(GlobalEnv.GetTempFile(), GlobalEnv.GetHttpx5xx())
                Files.RemoveDuplicateFromFile(GlobalEnv.GetHttpx5xx())
            i += 1
        urls = Files.ExtractUrlsFromFile(GlobalEnv.GetHttpx())
        Files.WriteListToFile(GlobalEnv.GetEnhancedHttpx(), 'a', urls)
        Files.RemoveDuplicateFromFile(GlobalEnv.GetEnhancedHttpx())

    def Execute(self):
        self.__CrtSh()
        self.__Subfinder()
        self.__Sublist3r()
        self.__AssetFinder()
        self.__Chaos()
        # self.__Amass()
        self.__Httpx()
