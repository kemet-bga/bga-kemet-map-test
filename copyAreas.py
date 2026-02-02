#! python3.13
# This script was generated with the help of ChatGPT

try:
    import os
    from PIL import Image

    # Determine script directory (script can be launched from anywhere)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Transparency multiplier for overlay alpha (30%)
    OVERLAY_ALPHA = 0.3

    # Map variants to process
    map_variants = [2, 3, 4, 5]

    for variant in map_variants:
        print(f"\nProcessing map{variant}p...")

        base_dir = os.path.normpath(
            os.path.join(script_dir, f"../drafts/img/map/export/borderedAreas/areas{variant}p")
        )
        overlay_dir = os.path.normpath(
            os.path.join(script_dir, f"../drafts/img/map/export/areas/areas{variant}p")
        )
        output_dir = os.path.normpath(
            os.path.join(script_dir, f"./img/map/areas/map{variant}p")
        )

        os.makedirs(output_dir, exist_ok=True)

        if not os.path.isdir(base_dir):
            print(f"Base directory not found: {base_dir}")
            continue

        for filename in os.listdir(base_dir):
            if not filename.lower().endswith(".png"):
                continue

            base_path = os.path.join(base_dir, filename)
            overlay_path = os.path.join(overlay_dir, filename)
            output_path = os.path.join(output_dir, filename)

            if not os.path.isfile(overlay_path):
                print(f"Overlay not found for {filename}, skipping")
                continue

            try:
                with Image.open(base_path).convert("RGBA") as base_img, \
                     Image.open(overlay_path).convert("RGBA") as overlay_img:

                    # Ensure same size (alpha_composite requires identical sizes)
                    if overlay_img.size != base_img.size:
                        print(f"Size mismatch for {filename}: base={base_img.size}, overlay={overlay_img.size}, skipping")
                        continue

                    # Take ONLY the alpha channel from the overlay (ignore its RGB completely)
                    overlay_alpha = overlay_img.getchannel("A")

                    # Apply global transparency multiplier (OVERLAY_ALPHA)
                    overlay_alpha = overlay_alpha.point(lambda p: int(p * OVERLAY_ALPHA))

                    # Create a "white overlay" image with that alpha mask
                    # RGB is forced to white, alpha is taken from overlay_alpha
                    white_overlay = Image.new("RGBA", base_img.size, (255, 255, 255, 0))
                    white_overlay.putalpha(overlay_alpha)

                    # Composite: base + (white overlay with alpha from overlay)
                    result = Image.alpha_composite(base_img, white_overlay)

                    # Save result
                    result.save(output_path, "PNG")
                    print(f"Saved: {output_path}")

            except Exception as img_error:
                print(f"Error processing {filename}: {img_error}")

    print("\nDone.")

except Exception as e:
    print("Fatal error:", e)

input("\nPress Enter to exit...")
