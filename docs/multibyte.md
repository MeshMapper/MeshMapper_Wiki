# Multi-Byte Repeaters

Every packet that travels through a MeshCore mesh network carries a record of its journey — a list of the repeaters it passed through. Each repeater stamps the packet with the prefix of its Public ID, called a **hop**.

MeshMapper fully supports multi-byte hops in the wardriving app, the map, and packet analyzer.

---

## The 1-Byte Problem

In 1-byte mode, repeaters are identified by just the first two hex characters of their Public ID (e.g., `A1`, `4F`, `09`). With only **254 possible combinations** (hex `01` to `FE` — `00` and `FF` are reserved by MeshCore firmware), growing regions inevitably see two different repeaters sharing the same ID.

When this happens, MeshMapper can't tell which physical repeater was actually involved in a packet's path. It enters a quarantine mode for the affected devices to protect data integrity.

!!! tip "Learn More About Collisions"
    For a detailed explanation of how MeshMapper detects, handles, and resolves duplicate repeater IDs, see [Duplicate Repeater IDs](duplicaterepeaterid.md).

## Upgrading to Multi-Byte

Upgrading a region from 1-byte to multi-byte hops is a gradual process — you don't need to update every device at once.  Repeaters upgraded to the latest multi-byte capable firmware will still relay packets from repeaters and companions running older 1-byte firmware.

### Step 1: Update Firmware

Flash repeaters and companion devices with **MeshCore firmware v1.14.1 or newer**. The firmware's hop byte configuration must be set to 2 or 3 bytes. 

In the command line console on the repeater, for 2-byte, set:
```
set path.hash.mode 1
```
and for 3-byte:
```
set path.hash.mode 2
```

When done, reboot the device, then **send a flood advert**.  This will "upgrade" the repeater in MeshMapper to multi-byte capable automatically.

Repeaters and companions in the region should be running the same configuration.

### Step 2: Update Region Settings

When the majority of a regions repeaters have been upgraded to a multi-byte capable firmware, in the region's admin panel, go to **Settings** and set the **Hop Bytes** value to match your regions configuration. Changing this value triggers an automatic collision recalculation across all repeaters in the region.  (You must be an administrator of your region in order to access this setting)

### Step 3: Automatic Detection and Upgrade

As updated repeaters relay packets, MeshMapper detects the longer hop IDs automatically. It tracks hop bytes **per repeater** — so each device's byte length updates individually as it's heard on the network.

For example, if repeater `A1B2C3D4E5F6` was previously known as a 1-byte device (hop ID `A1`), the first time it's heard with a 2-byte hop (`A1B2`), MeshMapper updates its record. No manual intervention needed.

!!! note "Mixed Environments"
    During a transition period, a region may have a mix of 1-byte and 2/3-byte repeaters. MeshMapper handles this gracefully — it uses each repeater's individually tracked hop byte value for collision detection and path resolution. Two repeaters that collide at 1 byte may be perfectly distinguishable at 2 bytes.

!!! note "Packet Types"
    Not all packet types are ingested into the MeshMapper engine responsible for processing repeater upgrades.  In order for a repeater to automatically upgrade to 2 or 3-byte capable within MeshMapper, its ID must be contained within the path of an **advert** or **wardriving** packet.  Public messages or other packet types (trace, request, etc.) will not result in an automatic upgrade.

### Smart Collision Resolution

As repeaters upgrade, collisions that existed in 1-byte mode may automatically resolve:

- Repeater `AB` (1-byte) and repeater `AB` (1-byte) **are** in collision — indistinguishable.
- After upgrading, repeater `AB12` (2-byte) and repeater `AB9F` (2-byte) are **no longer** in collision — the longer IDs differentiate them.

MeshMapper re-evaluates collisions as hop bytes update, restoring previously excluded repeaters to active status when they become distinguishable.

### Filtering by Hop Bytes

The map's advanced filter panel includes a **Hop Bytes** filter, allowing you to view only repeaters of a specific byte length. This is helpful for tracking firmware upgrade progress across your region — quickly see which repeaters are still running 1-byte firmware and need updating.  In addition, a list of repeaters and their byte modes/capabilities can be found in the **Region Info** page under **Repeaters**.