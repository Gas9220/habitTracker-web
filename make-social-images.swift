// Draws each language's picture for links to the site shared elsewhere (og:image): the icon, the
// page's title and tagline, and the habit list in a phone, 1200 × 630, into images/<lang>/social.jpg.
// Run it again after changing those strings or the screenshots:
//
//     swift make-social-images.swift

import AppKit

let root = URL(fileURLWithPath: #filePath).deletingLastPathComponent()
let size = NSSize(width: 1200, height: 630)
let text = NSColor(srgbRed: 0x1d / 255, green: 0x1d / 255, blue: 0x1f / 255, alpha: 1)
let secondary = NSColor(srgbRed: 0x5c / 255, green: 0x64 / 255, blue: 0x70 / 255, alpha: 1)

/// A string from the site, without its HTML.
func plain(_ html: String) -> String {
    html.replacingOccurrences(of: "<br>", with: " ")
        .replacingOccurrences(of: "<[^>]+>", with: "", options: .regularExpression)
}

let icon = NSImage(contentsOf: root.appending(path: "images/app-icon.png"))!

for language in ["en", "it", "fr", "es"] {
    let data = try Data(contentsOf: root.appending(path: "src/strings/\(language).json"))
    let strings = try JSONSerialization.jsonObject(with: data) as! [String: String]
    let screenshot = NSImage(contentsOf: root.appending(path: "images/\(language)/habits.png"))!

    let image = NSBitmapImageRep(
        bitmapDataPlanes: nil, pixelsWide: Int(size.width), pixelsHigh: Int(size.height),
        bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
        colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0
    )!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: image)

    NSGradient(starting: NSColor(srgbRed: 0.91, green: 0.95, blue: 1, alpha: 1), ending: .white)!
        .draw(in: NSRect(origin: .zero, size: size), angle: -90)

    icon.draw(in: NSRect(x: 80, y: 410, width: 140, height: 140))
    NSAttributedString(string: plain(strings["hero_title"]!), attributes: [
        .font: NSFont.systemFont(ofSize: 60, weight: .bold),
        .foregroundColor: text,
    ]).draw(in: NSRect(x: 80, y: 190, width: 660, height: 190))
    NSAttributedString(string: strings["og_description"]!, attributes: [
        .font: NSFont.systemFont(ofSize: 28),
        .foregroundColor: secondary,
    ]).draw(in: NSRect(x: 80, y: 60, width: 660, height: 120))

    // The phone, as the site draws it: a dark frame around the screen.
    let phoneHeight: CGFloat = 570
    let phone = NSRect(x: 870, y: 30, width: phoneHeight * 660 / 1434, height: phoneHeight)
    text.setFill()
    NSBezierPath(roundedRect: phone, xRadius: 40, yRadius: 40).fill()
    let screen = phone.insetBy(dx: 8, dy: 8)
    NSGraphicsContext.saveGraphicsState()
    NSBezierPath(roundedRect: screen, xRadius: 33, yRadius: 33).addClip()
    screenshot.draw(in: screen)
    NSGraphicsContext.restoreGraphicsState()

    NSGraphicsContext.restoreGraphicsState()
    let jpeg = image.representation(using: .jpeg, properties: [.compressionFactor: 0.85])!
    try jpeg.write(to: root.appending(path: "images/\(language)/social.jpg"))
    print("wrote images/\(language)/social.jpg")
}
