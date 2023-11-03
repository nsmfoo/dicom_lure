# dicom_lure


### Background:

This is the story of yet another failed research of mine (don't get me started). But I might as well documents it and perhaps it might even be somewhat useful in a way that I can't imagine too someone else.

I had an idea a while back, that I dusted of a couple of months ago. The idea was to see if there where a "natural" way for a Dicom image or rather, the viewer to populate or extend metadata automatically when accessed. The thought was to use that as method to detect an adversary accessing an image.

Here might be a good time to once again highlight that I really have no clue what I'm doing and I don't work in meditech, apparently the lack of insight did not stop me ...

So having looked at the Dicom image specification and played around a bit with the metadata.. I decided that I could not find a way to trigger a download/beacon of any sort. Which was sad as this could have been my conference talk for the rest of the year (I'm just kidding).

So having that route lead to nowhere, I remembered that I did stumble across the possibility to embed PDF files in a Dicom image.

So trying to get something out of all of this. I decided to follow that route and here we are.

### About

dicom_lure is a stand a lone script for creating an Dicom image with an embedded PDF (which is nothing fancy and fully supported by the specification). But what if the PDF is a honeytoken?

The lure can be used in your own infrastructure or used with dicompot (https://github.com/nsmfoo/dicompot)

### Use cases: 

After having spend some time looking at this, I came up with the following two scenarios to justify the time I spend/wasted (they are admittedly a bit vague)

- Catch insiders: Apparently it happens from time to time that employees have a hard time not looking at medical journals of the rich and famous. This could be a way to detect that.

- Catch external intruders accessing your data.

### What to embed?:

- PDF with a password set. Waste the time of an intruder

- Canary PDF embedded, default causes a warning about an external resource being accessed (in modern PDF viewers that "support" that type of beacon). All Dicom viewers that I have tested, rely on the OS default PDF viewer

- Canary Webtoken URL in the PDF text (needs to be clicked on), works fine (using custom domain would yield better results)

- or a PDF with an URL (in the text) pointing to a system or service setup only for the "lure", which would not be a dead give away and result in the same level of detection as the Canary Webtoken

- PDF with a watermark/unique phrase, detect if it shows up on a search engine (needs to be exported from the image)

- Or a combination of the above, mix and match as you see fit

### Usage:
```
dicom_lure.py [-h] -T TEMPLATE_FILE -E PDF_FILE -O OUTPUT_FILE [-N TITLE_NAME]
```
### Example: 
```
python3 dicom_lure.py -T template.dcm -E canary.pdf -O lure.dcm -N sensitive
```
### Script output: 

```
-[ Reading template file: template.dcm
-[ Reading PDF file: canary.pdf
-[ Applying a custom title name: sensitive
-[ Lure file created: lure.dcm
```
### Known issues a.k.a Good to know:

- RadiAnt DICOM Viewer
    -  can handle PDF's with passwords (macOS created PDF)
- Rubo Viewer
    - can't handle PDF's with passwords (macOS created PDF)
- Horos
    - Horos
- can't handle PDF's with passwords (macOS created PDF)

These issues might come from how and what metadata is added to the image. 