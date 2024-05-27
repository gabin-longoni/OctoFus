set ffDecJar="C:\Program Files (x86)\FFDec\ffdec.jar"
set dofInvoker="C:\Users\%USERNAME%\AppData\Local\Ankama\Dofus\DofusInvoker.swf"
set pathDecompile="%~dp0sources"
if not exist %pathDecompile% mkdir %pathDecompile%

java -jar %ffDecJar% -selectclass com.ankamagames.dofus.network.++,com.ankamagames.dofus.datacenter.++ -export script %pathDecompile% %dofInvoker%