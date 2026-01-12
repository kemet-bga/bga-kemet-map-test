# This script was generated with the help of ChatGPT

try:
    import os
    from PIL import Image

    # Determine script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Transparency level for overlay (30%)
    OVERLAY_ALPHA = 0.3

    # Map variants to process
    map_variants = [2, 3, 4, 5]

    for variant in map_variants:
        print(f"\nProcessing map{variant}p...")

        base_dir = os.path.normpath(
            os.path.join(script_dir, f"../drafts/assets/img/map/map{variant}p/areas")
        )
        overlay_dir = os.path.normpath(
            os.path.join(script_dir, f"../drafts/assets/img/map/map{variant}p/filledAreas")
        )
        output_dir = os.path.normpath(
            os.path.join(script_dir, f"./img/map/map{variant}p/areas")
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

                    # Apply transparency to overlay
                    alpha = overlay_img.split()[3].point(
                        lambda p: int(p * OVERLAY_ALPHA)
                    )
                    overlay_img.putalpha(alpha)

                    # Composite images
                    result = Image.alpha_composite(base_img, overlay_img)

                    # Save result
                    result.save(output_path, "PNG")
                    print(f"Saved: {output_path}")

            except Exception as img_error:
                print(f"Error processing {filename}: {img_error}")

    print("\nDone.")

except Exception as e:
    print("Fatal error:", e)

input("\nPress Enter to exit...")
