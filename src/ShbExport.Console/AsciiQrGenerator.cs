using QRCoder;

namespace ShbExport.Console;

public class AsciiQrGenerator
{
    QRCodeGenerator _qrGenerator = new();
    public string GenerateAsciiQrCode(string content)
    {
        QRCodeData qrCodeData = _qrGenerator.CreateQrCode(content, QRCodeGenerator.ECCLevel.Q);
        AsciiQRCode qrCode = new AsciiQRCode(qrCodeData);
        return qrCode.GetGraphicSmall();
    }
}