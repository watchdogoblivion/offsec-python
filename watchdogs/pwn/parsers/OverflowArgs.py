# author: WatchDogOblivion
# description: TODO
# WatchDogs Overflow Arguments

from watchdogs.base.models.Args import Args
from watchdogs.utils.Constants import EMPTY


class OverflowArgs(Args):

  VERSION = "Request version: 1.0"

  def __init__(self, process=EMPTY, localProcess=False, remoteHost="localhost", remotePort=7411,
               operatingSystem="linux", arch="i386", archBytes=4, bufferSize=112, bufferCharacter=b"A",
               basePointer=b"/bin/sh\x00", instructionPointer=b"", memoryAddress=b""):
    #type: (str, bool, str, int, str, str, int, int, bytes, bytes, bytes, bytes) -> None
    super(OverflowArgs, self).__init__()
    self.process = process
    self.localProcess = localProcess
    self.remoteHost = remoteHost
    self.remotePort = remotePort
    self.operatingSystem = operatingSystem
    self.arch = arch
    self.archBytes = archBytes
    self.bufferSize = bufferSize
    self.bufferCharacter = bufferCharacter
    self.basePointer = basePointer
    self.instructionPointer = instructionPointer
    self.memoryAddress = memoryAddress

  def getVersion(self):  #type: () -> str
    return OverflowArgs.VERSION

  def addArguments(self):  #type: () -> OverflowArgs
    parser = self.getParser()
    parser.add_argument("-p", "--process", type=str, metavar=EMPTY, default=EMPTY)
    parser.add_argument("-lp", "--local-process", action="store_true", default=False)
    parser.add_argument("-rh", "--remote-host", type=str, metavar=EMPTY, default="localhost")
    parser.add_argument("-rp", "--remote-port", type=int, metavar=EMPTY, default=7411)
    parser.add_argument("-os", "--operating-system", type=str, metavar=EMPTY, default="linux")
    parser.add_argument("-a", "--arch", type=str, metavar=EMPTY, default="i386")
    parser.add_argument("-ab", "--arch-bytes", type=int, metavar=EMPTY, default=4)
    parser.add_argument("-bs", "--buffer-size", type=int, metavar=EMPTY, default=112)
    parser.add_argument("-bc", "--buffer-character", type=bytes, metavar=EMPTY, default=b"A")
    parser.add_argument("-bp", "--base-pointer", type=bytes, metavar=EMPTY, default=b"bash")
    parser.add_argument("-ip", "--instruction-pointer", type=bytes, metavar=EMPTY, default=b"")
    parser.add_argument("-ma", "--memory-address", type=bytes, metavar=EMPTY, default=b"")

    return self