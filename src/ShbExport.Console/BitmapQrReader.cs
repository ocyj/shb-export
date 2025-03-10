using ZXing.ImageSharp;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.PixelFormats;

namespace ShbExport.Console;

public static class BitmapQrReader
{

    public static string ReadQrCode(string bitmapFilePath)
    {
        string filePath = bitmapFilePath;

        // 1) Load the image using ImageSharp
        using Image<Rgba32> image = Image.Load<Rgba32>(filePath);

        // 2) Use the ImageSharp-based barcode reader
        var barcodeReader = new BarcodeReader<Rgba32>();

        // 3) Decode
        var result = barcodeReader.Decode(image);


        // 3) Check the results
        if (result != null)
        {
            return result.Text;
        }

        return string.Empty;
    }

}