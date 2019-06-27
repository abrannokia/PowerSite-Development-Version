use Projects


/* import BDR */
delete from BDR2G

bulk insert [dbo].[BDR2G]
from 'C:\Users\abran\OneDrive - Nokia\NOKIA SHARED FOLDER AB\Projects\2019\Traitment Flux OAL 20190131\INPUT\BDR2G.csv'
with (fieldterminator = ';', rowterminator = '\n')
go



/* import SFR */
delete from SFR

bulk insert [dbo].[SFR]
from 'C:\Users\abran\OneDrive - Nokia\NOKIA SHARED FOLDER AB\Projects\2019\Traitment Flux OAL 20190131\INPUT\SFR.csv'
with (fieldterminator = 'Â¤', rowterminator = '0x0a')
go


/* import BYTEL */
delete from BYTEL

bulk insert [dbo].[BYTEL]
from 'C:\Users\abran\OneDrive - Nokia\NOKIA SHARED FOLDER AB\Projects\2019\Traitment Flux OAL 20190131\INPUT\BYTEL.csv'
with (fieldterminator = 'Â¤', rowterminator = '0x0a')
go